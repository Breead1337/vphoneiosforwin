// Find scalar constant used in code (via decompiler pcode is overkill; use instruction scan on the raw value in operands)
// args: <hexval>  -- prints functions whose instructions reference the value as an address/immediate through refs
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
public class Const extends GhidraScript {
  public void run() throws Exception {
    long v = Long.parseUnsignedLong(getScriptArgs()[0].replace("0x",""),16);
    Address t = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v);
    ReferenceManager rm = currentProgram.getReferenceManager();
    FunctionManager fm = currentProgram.getFunctionManager();
    for (Reference r : rm.getReferencesTo(t)) {
      Function f = fm.getFunctionContaining(r.getFromAddress());
      println(r.getFromAddress()+" "+(f==null?"?":f.getName()+" @ "+f.getEntryPoint())+" "+r.getReferenceType());
    }
  }
}
