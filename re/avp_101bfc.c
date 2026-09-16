// ===== 0x101bfc -> FUN_00101bfc @ 00101bfc

void FUN_00101bfc(undefined8 param_1,undefined8 param_2,ulong param_3,long param_4,
                 undefined8 param_5)

{
  undefined1 uVar1;
  int iVar2;
  ulong uVar3;
  undefined8 uVar4;
  ulong uVar5;
  undefined8 extraout_x8;
  ulong unaff_x19;
  undefined1 auVar6 [16];
  ulong local_60;
  undefined8 local_58;
  
  auVar6 = FUN_00102af4();
  uVar3 = auVar6._0_8_;
  if ((uVar3 == 0) || (param_4 == 0)) {
                    /* WARNING: Subroutine does not return */
    FUN_0010550c();
  }
  if (uVar3 < auVar6._8_8_ || param_3 <= uVar3) {
LAB_00101d88:
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  local_58 = extraout_x8;
  FUN_00102b58();
  if (*(int *)(uVar3 + 8) == 0x4d656d7a) {
    thunk_FUN_00102b40(*(undefined8 *)(uVar3 + 0x10),*(undefined8 *)(uVar3 + 0x18),
                       *(undefined8 *)(uVar3 + 0x20),*(undefined8 *)(uVar3 + 0x28));
    local_60 = 0;
    uVar1 = unaff_x19 == 0x1d;
    if (unaff_x19 < 0x1e) {
      uVar4 = 0x40040020;
    }
    else {
      FUN_00102b24(&local_60);
      iVar2 = FUN_00102b68();
      if (iVar2 == 0) {
        uVar1 = local_60 == unaff_x19;
        if (local_60 <= unaff_x19) {
          uVar1 = param_4 == *(long *)(uVar3 + 0x10);
          if (!(bool)uVar1) {
            FUN_00111434(param_4,param_5);
          }
          goto LAB_00101ca8;
        }
        uVar4 = 0x40040022;
      }
      else {
        uVar4 = 0x40040021;
      }
    }
    FUN_001275ac(uVar4);
    uVar4 = 0x4004001e;
  }
  else {
    uVar1 = *(int *)(uVar3 + 8) == 0x696d6734;
    if ((bool)uVar1) {
      uVar5 = *(ulong *)(uVar3 + 0x20);
      auVar6 = FUN_00102ab4(*(undefined8 *)(uVar3 + 0x10),*(undefined8 *)(uVar3 + 0x18),uVar5,
                            *(undefined8 *)(uVar3 + 0x28));
      uVar3 = auVar6._0_8_;
      if (uVar3 < auVar6._8_8_ || uVar5 <= uVar3) goto LAB_00101d88;
      FUN_00102c0c(*(undefined8 *)(uVar3 + 0x40),*(undefined8 *)(uVar3 + 0x48),
                   *(undefined8 *)(uVar3 + 0x50),*(undefined8 *)(uVar3 + 0x58));
      iVar2 = FUN_001262f8();
      uVar1 = iVar2 == (int)unaff_x19;
      if ((bool)uVar1) {
LAB_00101ca8:
        uVar4 = 0;
        goto LAB_00101d2c;
      }
      uVar4 = 0x4004001d;
    }
    else {
      uVar4 = 0x4004001f;
    }
  }
  FUN_001275ac(uVar4);
  uVar4 = 0xffffffff;
LAB_00101d2c:
  FUN_00102ad0(local_58,uVar4);
  if ((bool)uVar1) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


