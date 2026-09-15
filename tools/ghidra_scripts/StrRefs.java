// Find literal strings in memory (byte search), list referencing functions, optionally decompile them.
// args: <outfile|-> <literal>[|<literal>...] [decompile=1]
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.util.*;

public class StrRefs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        boolean dec = a.length > 2 && a[2].equals("1");
        PrintWriter out = a[0].equals("-") ? null : new PrintWriter(new FileWriter(a[0], true));
        DecompInterface d = new DecompInterface();
        d.openProgram(currentProgram);
        Set<Function> done = new LinkedHashSet<>();
        ReferenceManager rm = currentProgram.getReferenceManager();
        FunctionManager fm = currentProgram.getFunctionManager();
        Memory mem = currentProgram.getMemory();
        for (String lit : a[1].split("\\|")) {
            byte[] pat = lit.getBytes("UTF-8");
            Address at = mem.getMinAddress();
            while (at != null) {
                at = mem.findBytes(at, pat, null, true, monitor);
                if (at == null) break;
                Address st = at;
                while (true) {
                    try {
                        if (mem.getByte(st.subtract(1)) == 0) break;
                        st = st.subtract(1);
                    } catch (Exception e) { break; }
                }
                println("STR " + st + " (" + lit + ")");
                List<Address> froms = new ArrayList<>();
                for (Reference r : rm.getReferencesTo(st)) froms.add(r.getFromAddress());
                for (Reference r : rm.getReferencesTo(st)) {
                    Data dd = getDataContaining(r.getFromAddress());
                    if (dd != null) for (Reference r2 : rm.getReferencesTo(dd.getAddress())) froms.add(r2.getFromAddress());
                }
                for (Address f : froms) {
                    Function fn = fm.getFunctionContaining(f);
                    println("    ref " + f + " in " + (fn == null ? "?" : fn.getName() + " @ " + fn.getEntryPoint()));
                    if (fn != null) done.add(fn);
                }
                at = at.add(1);
            }
        }
        if (dec && out != null) {
            for (Function f : done) {
                DecompileResults r = d.decompileFunction(f, 180, monitor);
                out.println("// ===== " + f.getName() + " @ " + f.getEntryPoint());
                out.println(r.decompileCompleted() ? r.getDecompiledFunction().getC() : "// FAILED");
            }
        }
        if (out != null) out.close();
    }
}
