// List every reference into [start,end): "fromAddr func -> toAddr type"
// args: <start> <end>   (hex)
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.util.*;

public class Xrefs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        AddressSpace sp = currentProgram.getAddressFactory().getDefaultAddressSpace();
        long s = Long.parseUnsignedLong(a[0].replace("0x", ""), 16), e = Long.parseUnsignedLong(a[1].replace("0x", ""), 16);
        ReferenceManager rm = currentProgram.getReferenceManager();
        FunctionManager fm = currentProgram.getFunctionManager();
        TreeMap<Long, List<String>> byTo = new TreeMap<>();
        AddressIterator it = rm.getReferenceDestinationIterator(sp.getAddress(s), true);
        while (it.hasNext()) {
            Address to = it.next();
            if (Long.compareUnsigned(to.getOffset(), e) >= 0) break;
            for (Reference r : rm.getReferencesTo(to)) {
                Function f = fm.getFunctionContaining(r.getFromAddress());
                byTo.computeIfAbsent(to.getOffset(), k -> new ArrayList<>()).add(
                    r.getFromAddress() + " " + (f == null ? "?" : f.getName()) + " " + r.getReferenceType());
            }
        }
        for (Map.Entry<Long, List<String>> en : byTo.entrySet()) {
            println(String.format("%#x:", en.getKey()));
            for (String x : en.getValue()) println("    " + x);
        }
    }
}
