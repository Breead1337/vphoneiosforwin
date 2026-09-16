// ===== 0x0011f65c -> FUN_0011f644 @ 0011f644

void FUN_0011f644(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  code *pcVar1;
  uint *puVar2;
  undefined8 uVar3;
  uint *puVar4;
  ulong unaff_x30;
  undefined1 auVar5 [16];
  
  if (((uint)param_2 - 8 & 0xff) < 0xf9) {
    uVar3 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
    FUN_00105548(uVar3,0x8e0);
  }
  puVar4 = (uint *)(ulong)((uint)param_2 | 4);
  auVar5 = FUN_00120208(param_1,0xff);
  puVar2 = auVar5._0_8_;
  if (auVar5._8_8_ <= puVar2 && puVar2 < puVar4) {
    if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
      pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x11f6b0);
      (*pcVar1)();
    }
    FUN_00120344(*puVar2 >> 0x1c,param_3,param_2,*puVar2 & 0x3ff);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


