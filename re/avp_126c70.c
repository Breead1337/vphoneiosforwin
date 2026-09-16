// ===== 0x00126c70 -> FUN_00126c70 @ 00126c70

undefined8 FUN_00126c70(long param_1)

{
  code *pcVar1;
  undefined8 uVar2;
  ulong unaff_x30;
  ulong in_stack_00000000;
  ulong in_stack_00000008;
  
  if ((long)in_stack_00000000 < 0) {
    uVar2 = FUN_00126f7c();
                    /* WARNING: Subroutine does not return */
    FUN_00105548(uVar2,0x1d);
  }
  if (((in_stack_00000000 < *(ulong *)(param_1 + 0x20)) &&
      (!CARRY8(in_stack_00000000,in_stack_00000008))) &&
     (!SCARRY8(in_stack_00000000,*(long *)(param_1 + 0x68)))) {
    FUN_00126f54(*(undefined8 *)(param_1 + 0x60));
    if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
      pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x126cdc);
      (*pcVar1)();
    }
    uVar2 = FUN_001262f8();
    return uVar2;
  }
  return 0;
}


