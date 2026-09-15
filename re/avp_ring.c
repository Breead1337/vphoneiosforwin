// ===== 0x106af0 -> FUN_00106af0 @ 00106af0

void FUN_00106af0(void)

{
  return;
}


// ===== 0x106bc4 -> FUN_00106bc4 @ 00106bc4

void FUN_00106bc4(void)

{
  long lVar1;
  
  lVar1 = FUN_00106b48();
  if (lVar1 != 0) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0010550c();
}


// ===== 0x1068ac -> FUN_001068ac @ 001068ac

void FUN_001068ac(undefined8 param_1,undefined8 param_2,long *param_3)

{
  ulong uVar1;
  long *plVar2;
  code *extraout_x9;
  undefined1 auVar3 [16];
  
  FUN_00106af0();
  auVar3 = FUN_00106bc4();
  plVar2 = auVar3._0_8_;
  if (auVar3._8_8_ <= plVar2 && plVar2 < param_3) {
    if (*plVar2 == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_0010550c();
    }
    uVar1 = plVar2[0xf];
    if ((ulong)plVar2[0x10] <= uVar1 && uVar1 < (ulong)plVar2[0x11]) {
      if (*(long *)(uVar1 + 0x18) != 0) {
        FUN_00106ac0();
        (*extraout_x9)();
        return;
      }
                    /* WARNING: Subroutine does not return */
      FUN_0012e944();
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x106ac0 -> FUN_00106ac0 @ 00106ac0

undefined1  [16] FUN_00106ac0(long param_1)

{
  undefined1 auVar1 [16];
  
  auVar1._8_8_ = param_1 + 0x68;
  auVar1._0_8_ = param_1 + 0x68;
  return auVar1;
}


// ===== 0x1280a0 -> FUN_001280a0 @ 001280a0

void FUN_001280a0(void)

{
  code *pcVar1;
  ulong unaff_x30;
  
  thunk_FUN_00100370();
  if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
    pcVar1 = (code *)SoftwareBreakpoint(0xc471,0x1280c4);
    (*pcVar1)();
  }
  FUN_00100430();
  return;
}


// ===== 0x1280c8 -> FUN_001280c8 @ 001280c8

bool FUN_001280c8(long param_1,ulong param_2)

{
  long lVar1;
  
  lVar1 = FUN_001280a0();
  return param_2 <= (ulong)(lVar1 - param_1);
}


