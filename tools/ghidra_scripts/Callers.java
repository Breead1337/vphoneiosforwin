// Print call tree upward (callers) for functions containing the given addresses, depth 4.
// args: <addr> [...]
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import java.util.*;

public class Callers extends GhidraScript {
    void up(Function f, int depth, Set<Function> seen) {
        if (depth > 4 || !seen.add(f)) return;
        for (Function c : f.getCallingFunctions(monitor)) {
            println("  ".repeat(depth) + "<- " + c.getName() + " @ " + c.getEntryPoint());
            up(c, depth + 1, seen);
        }
    }
    @Override
    public void run() throws Exception {
        for (String s : getScriptArgs()) {
            Address ad = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(s);
            Function f = currentProgram.getFunctionManager().getFunctionContaining(ad);
            if (f == null) { println("no func " + s); continue; }
            println(f.getName() + " @ " + f.getEntryPoint());
            up(f, 1, new HashSet<>());
        }
    }
}
