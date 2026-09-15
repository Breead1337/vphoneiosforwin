// ===== 0x1068d8 -> FUN_001068ac @ 001068ac

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


// ===== 0x10d5c4 -> FUN_0010d5c4 @ 0010d5c4

undefined8 FUN_0010d5c4(void)

{
  undefined8 *puVar1;
  uint *puVar2;
  uint uVar3;
  undefined1 in_ZR;
  int iVar4;
  long lVar5;
  undefined8 uVar6;
  long *unaff_x20;
  long *unaff_x21;
  long *unaff_x22;
  undefined8 *unaff_x23;
  undefined8 *unaff_x24;
  undefined8 *unaff_x25;
  int unaff_w27;
  
  FUN_0010d88c();
  if (!(bool)in_ZR) {
    uVar6 = FUN_0010d800();
                    /* WARNING: Subroutine does not return */
    FUN_00105548(uVar6,0x9d);
  }
  FUN_0010d870();
  if ((bool)in_ZR) {
    lVar5 = 0;
  }
  else {
    lVar5 = FUN_001280a0();
  }
  if (unaff_x21 <= unaff_x22 && unaff_x22 < unaff_x20) {
    while (puVar2 = (uint *)unaff_x22[8],
          (uint *)unaff_x22[9] <= puVar2 && puVar2 < (uint *)unaff_x22[10]) {
      uVar3 = *(uint *)(*unaff_x22 + (ulong)*puVar2);
      if ((uVar3 & 0xc0000) != 0) {
        uVar6 = FUN_0010d800();
                    /* WARNING: Subroutine does not return */
        FUN_00105548(uVar6,0x81);
      }
      if ((uVar3 >> 0x10 & 1) == 0) {
        if (unaff_x24 <= unaff_x23 && unaff_x23 < unaff_x25) {
          puVar1 = (undefined8 *)(*unaff_x22 + (ulong)puVar2[2]);
          uVar3 = *(uint *)(unaff_x23 + 1);
          *puVar1 = *unaff_x23;
          puVar1[1] = (ulong)uVar3;
          FUN_0010d814();
          return 0;
        }
        break;
      }
      if (unaff_w27 == 0) {
        return 0xffffffff;
      }
      if ((lVar5 != 0) && (iVar4 = FUN_001280c8(lVar5), iVar4 != 0)) {
        FUN_0010d844(0xae);
        return 0xfffffffe;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x10d88c -> FUN_0010d88c @ 0010d88c

void FUN_0010d88c(void)

{
  undefined8 in_x4;
  undefined8 in_x5;
  undefined8 in_x6;
  undefined8 in_x7;
  
  FUN_0010d7f4(in_x4,in_x5,in_x6,in_x7);
  return;
}


// ===== 0x10d7f4 -> FUN_0010d7f4 @ 0010d7f4

undefined1  [16] FUN_0010d7f4(undefined8 param_1,long param_2,long param_3,undefined8 param_4)

{
  code *pcVar1;
  undefined *puVar2;
  undefined8 uVar3;
  long *plVar4;
  uint uVar5;
  ulong uVar6;
  undefined **ppuVar7;
  undefined1 auVar8 [16];
  undefined8 uStack_90;
  long lStack_88;
  undefined8 uStack_70;
  long lStack_68;
  long lStack_60;
  undefined8 uStack_58;
  
  puVar2 = PTR_LOOP_0013d038;
  if (PTR_LOOP_0013d038 == (undefined *)0x0) {
    FUN_0012eab0(&DAT_0014684a);
                    /* WARNING: Does not return */
    pcVar1 = (code *)UndefinedInstructionException(0xc,0x12b9ec);
    (*pcVar1)();
  }
  uVar3 = FUN_0012ba14(&PTR_LOOP_0013d038);
  ppuVar7 = (undefined **)((ulong)puVar2 & 0xfffffffffffffff8);
  if (5 < (*(uint *)ppuVar7 & 7) - 1) goto switchD_0012b724_caseD_3;
  uVar6 = 3;
  switch(*(uint *)ppuVar7 & 7) {
  default:
    if (ppuVar7 != &PTR_LOOP_0013ce30) {
      uVar5 = 3;
      if ((ulong)ppuVar7[2] >> 0x23 == 0) {
        uVar5 = 1;
      }
      uVar6 = (ulong)uVar5;
      break;
    }
  case 3:
  case 4:
switchD_0012b724_caseD_3:
    uVar6 = 0;
    break;
  case 2:
  case 5:
    break;
  case 6:
    plVar4 = (long *)FUN_0012cb24(ppuVar7);
    uVar6 = 4;
    if ((ulong)ppuVar7[2] >> 0x23 == 0) {
      uVar5 = 4;
      if (*(ulong *)(*plVar4 + 0x10) >> 0x23 == 0) {
        uVar5 = 2;
      }
      uVar6 = (ulong)uVar5;
    }
  }
  if (param_3 != param_2) {
    if ((PTR_LOOP_0013d038 != (undefined *)0x0) && ((uint)uVar6 < 4)) {
      if (3 < uVar6) {
        uVar6 = 0;
      }
                    /* WARNING: Could not recover jumptable at 0x0012b7c0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      auVar8 = (*(code *)((long)(int)(&DAT_0012ba04)[uVar6] + 0x12b7b8))();
      return auVar8;
    }
    uStack_70 = param_1;
    lStack_68 = param_2;
    lStack_60 = param_3;
    uStack_58 = param_4;
    FUN_0012b264(&uStack_90,&uStack_70,&PTR_LOOP_0013d038,uVar3);
    param_1 = uStack_90;
    param_2 = lStack_88;
  }
  auVar8._8_8_ = param_2;
  auVar8._0_8_ = param_1;
  return auVar8;
}


// ===== 0x10d5ec -> FUN_0010d5c4 @ 0010d5c4

undefined8 FUN_0010d5c4(void)

{
  undefined8 *puVar1;
  uint *puVar2;
  uint uVar3;
  undefined1 in_ZR;
  int iVar4;
  long lVar5;
  undefined8 uVar6;
  long *unaff_x20;
  long *unaff_x21;
  long *unaff_x22;
  undefined8 *unaff_x23;
  undefined8 *unaff_x24;
  undefined8 *unaff_x25;
  int unaff_w27;
  
  FUN_0010d88c();
  if (!(bool)in_ZR) {
    uVar6 = FUN_0010d800();
                    /* WARNING: Subroutine does not return */
    FUN_00105548(uVar6,0x9d);
  }
  FUN_0010d870();
  if ((bool)in_ZR) {
    lVar5 = 0;
  }
  else {
    lVar5 = FUN_001280a0();
  }
  if (unaff_x21 <= unaff_x22 && unaff_x22 < unaff_x20) {
    while (puVar2 = (uint *)unaff_x22[8],
          (uint *)unaff_x22[9] <= puVar2 && puVar2 < (uint *)unaff_x22[10]) {
      uVar3 = *(uint *)(*unaff_x22 + (ulong)*puVar2);
      if ((uVar3 & 0xc0000) != 0) {
        uVar6 = FUN_0010d800();
                    /* WARNING: Subroutine does not return */
        FUN_00105548(uVar6,0x81);
      }
      if ((uVar3 >> 0x10 & 1) == 0) {
        if (unaff_x24 <= unaff_x23 && unaff_x23 < unaff_x25) {
          puVar1 = (undefined8 *)(*unaff_x22 + (ulong)puVar2[2]);
          uVar3 = *(uint *)(unaff_x23 + 1);
          *puVar1 = *unaff_x23;
          puVar1[1] = (ulong)uVar3;
          FUN_0010d814();
          return 0;
        }
        break;
      }
      if (unaff_w27 == 0) {
        return 0xffffffff;
      }
      if ((lVar5 != 0) && (iVar4 = FUN_001280c8(lVar5), iVar4 != 0)) {
        FUN_0010d844(0xae);
        return 0xfffffffe;
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x10d870 -> FUN_0010d870 @ 0010d870

void FUN_0010d870(void)

{
  return;
}


// ===== 0x12b6a4 -> FUN_0012b680 @ 0012b680

undefined1  [16]
FUN_0012b680(ulong param_1,byte *param_2,undefined8 param_3,long param_4,undefined8 param_5,
            ulong *param_6)

{
  code *pcVar1;
  undefined8 uVar2;
  long *plVar3;
  uint uVar4;
  ulong uVar5;
  undefined **ppuVar6;
  undefined1 auVar7 [16];
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined1 local_80 [16];
  long local_70;
  undefined8 uStack_68;
  
  if (param_2 != (byte *)0x0) {
    param_1 = (ulong)*param_2;
  }
  auVar7 = FUN_0012eab0(param_1,&DAT_0014684a);
  uVar5 = *param_6;
  if (uVar5 == 0) {
    FUN_0012eab0(&DAT_0014684a);
                    /* WARNING: Does not return */
    pcVar1 = (code *)UndefinedInstructionException(0xc,0x12b9ec);
    (*pcVar1)();
  }
  uVar2 = FUN_0012ba14(param_6);
  ppuVar6 = (undefined **)(uVar5 & 0xfffffffffffffff8);
  if (5 < (*(uint *)ppuVar6 & 7) - 1) goto switchD_0012b724_caseD_3;
  uVar5 = 3;
  switch(*(uint *)ppuVar6 & 7) {
  default:
    if (ppuVar6 != &PTR_LOOP_0013ce30) {
      uVar4 = 3;
      if ((ulong)ppuVar6[2] >> 0x23 == 0) {
        uVar4 = 1;
      }
      uVar5 = (ulong)uVar4;
      break;
    }
  case 3:
  case 4:
switchD_0012b724_caseD_3:
    uVar5 = 0;
    break;
  case 2:
  case 5:
    break;
  case 6:
    plVar3 = (long *)FUN_0012cb24(ppuVar6);
    uVar5 = 4;
    if ((ulong)ppuVar6[2] >> 0x23 == 0) {
      uVar4 = 4;
      if (*(ulong *)(*plVar3 + 0x10) >> 0x23 == 0) {
        uVar4 = 2;
      }
      uVar5 = (ulong)uVar4;
    }
  }
  if (param_4 != auVar7._8_8_) {
    if ((*param_6 != 0) && ((uint)uVar5 < 4)) {
      if (3 < uVar5) {
        uVar5 = 0;
      }
                    /* WARNING: Could not recover jumptable at 0x0012b7c0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      auVar7 = (*(code *)((long)(int)(&DAT_0012ba04)[uVar5] + 0x12b7b8))();
      return auVar7;
    }
    local_70 = param_4;
    uStack_68 = param_5;
    local_80 = auVar7;
    FUN_0012b264(&local_a0,local_80,param_6,uVar2);
    auVar7._8_8_ = uStack_98;
    auVar7._0_8_ = local_a0;
  }
  return auVar7;
}


