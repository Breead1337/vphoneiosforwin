// ===== 0x0012b6a4 -> FUN_0012b680 @ 0012b680

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


// ===== 0x00125974 -> FUN_00125454 @ 00125454

ulong FUN_00125454(ulong param_1,ulong param_2,ulong param_3,undefined8 param_4,ulong param_5)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  ulong uVar4;
  ulong uVar5;
  ulong uVar6;
  ulong uVar7;
  long lVar8;
  undefined8 uVar9;
  ulong uVar10;
  ulong uVar11;
  ulong extraout_x8;
  undefined8 uVar12;
  ulong extraout_x8_00;
  undefined1 auVar13 [16];
  undefined1 auVar14 [16];
  undefined1 auVar15 [16];
  ulong in_stack_00000000;
  ulong in_stack_00000008;
  long local_d8;
  undefined8 local_d0;
  ulong local_c8;
  ulong local_80;
  
  if ((long)in_stack_00000000 < 0) {
    uVar12 = 0x153;
    goto LAB_001259fc;
  }
  if (param_1 < param_2 || param_3 <= param_1) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  uVar10 = *(ulong *)(param_1 + 0x20);
  if ((uVar10 < in_stack_00000000 || uVar10 - in_stack_00000000 == 0) ||
     (CARRY8(in_stack_00000000,in_stack_00000008))) {
    return 0;
  }
  local_80 = uVar10 - in_stack_00000000;
  if (in_stack_00000000 + in_stack_00000008 <= uVar10) {
    local_80 = in_stack_00000008;
  }
  auVar13 = FUN_00126094();
  FUN_001268ec(auVar13._0_8_,auVar13._8_8_,param_3,param_4);
  FUN_00126094();
  uVar10 = param_3;
  uVar12 = param_4;
  uVar1 = FUN_001268ec();
  local_c8 = uVar10;
  local_d0 = uVar12;
  if ((in_stack_00000000 & (uint)~(-1 << (ulong)(uVar1 & 0x1f))) == 0) {
    FUN_00126070();
    uVar1 = FUN_00126958();
    local_c8 = uVar10;
    local_d0 = uVar12;
    if (((uint)~(-1 << (ulong)(uVar1 & 0x1f)) & param_5) != 0) goto LAB_0012552c;
    local_d0 = 0;
    local_c8 = 0;
    auVar13 = ZEXT816(0);
    uVar4 = 0;
  }
  else {
LAB_0012552c:
    FUN_00126094();
    FUN_001261d8();
    uVar1 = FUN_001268ec();
    FUN_00126094();
    FUN_001261d8();
    uVar4 = FUN_001268c8();
    FUN_00126094();
    FUN_001261d8();
    FUN_00125f5c();
    auVar13 = thunk_FUN_00126114();
    uVar10 = local_c8;
    uVar12 = local_d0;
    FUN_00126094();
    FUN_001261d8();
    FUN_001260bc();
    iVar2 = FUN_00126338();
    if (iVar2 < 1) {
      uVar11 = 0;
      goto LAB_001259bc;
    }
    uVar11 = (uVar4 & 0xffffffff) - (in_stack_00000000 & (uint)~(-1 << (ulong)(uVar1 & 0x1f)));
    uVar4 = local_80;
    if (uVar11 <= local_80) {
      uVar4 = uVar11;
    }
    FUN_00126154(param_5);
    FUN_00111154();
    in_stack_00000000 = in_stack_00000000 + uVar4;
    local_80 = local_80 - uVar4;
  }
  uVar11 = uVar4;
  if (local_80 != 0) {
    FUN_00126070();
    FUN_001268ec();
    FUN_001260d0();
    if ((in_stack_00000000 & extraout_x8) != 0) {
      uVar12 = 0x178;
      goto LAB_001259fc;
    }
  }
  while( true ) {
    local_d8 = auVar13._0_8_;
    FUN_00126070();
    uVar5 = FUN_001268c8();
    if (local_80 < (uVar5 & 0xffffffff)) break;
    auVar14 = FUN_00126094();
    uVar6 = FUN_001268ec(auVar14._0_8_,auVar14._8_8_,param_3,param_4);
    FUN_00126094();
    uVar5 = param_3;
    uVar12 = param_4;
    FUN_00126958();
    FUN_001260d0();
    uVar10 = (uint)((int)uVar4 + (int)param_5) & extraout_x8_00;
    if (uVar10 == 0) {
      FUN_00126154(param_5);
      thunk_FUN_00126114();
      FUN_001260e0();
      FUN_00126070();
      iVar2 = FUN_00126338();
      if (iVar2 < 1) goto LAB_001259bc;
    }
    else if (local_80 >> (uVar6 & 0x3f) < 2) {
      if (local_d8 == 0) {
        FUN_00126070();
        FUN_00125f5c();
        auVar13 = thunk_FUN_00126114();
        local_d0 = uVar12;
        local_c8 = uVar5;
      }
      FUN_00126070();
      FUN_001260bc();
      iVar2 = FUN_00126338();
      if (iVar2 < 1) goto LAB_001259bc;
      FUN_00126154(param_5);
      auVar14 = thunk_FUN_00126114();
      FUN_00126070();
      uVar1 = FUN_001268ec();
      FUN_00111434(auVar14._0_8_ + uVar4,auVar14._8_8_,uVar5,uVar12,auVar13._0_8_,auVar13._8_8_,
                   local_c8,local_d0,(long)(1 << (ulong)(uVar1 & 0x1f)));
    }
    else {
      FUN_00126154(param_5);
      auVar14 = thunk_FUN_00126114();
      uVar6 = uVar5;
      uVar9 = uVar12;
      FUN_001260f0();
      uVar7 = FUN_00126934();
      FUN_001260f0();
      iVar2 = FUN_00126338();
      if (iVar2 < 1) goto LAB_001259bc;
      FUN_00126154(param_5);
      auVar15 = thunk_FUN_00126114();
      FUN_001260f0();
      uVar1 = FUN_001268ec();
      FUN_00111434(auVar15._0_8_ + uVar4,auVar15._8_8_,uVar6,uVar9,
                   (auVar14._0_8_ + uVar4 + (uVar7 & 0xffffffff)) - uVar10,auVar14._8_8_,uVar5,
                   uVar12,(long)(iVar2 << (ulong)(uVar1 & 0x1f)));
    }
    auVar14 = FUN_00126094();
    uVar1 = FUN_001268ec(auVar14._0_8_,auVar14._8_8_,param_3,param_4);
    uVar4 = uVar4 + (long)(iVar2 << (ulong)(uVar1 & 0x1f));
    auVar14 = FUN_00126094();
    uVar1 = FUN_001268ec(auVar14._0_8_,auVar14._8_8_,param_3,param_4);
    FUN_00126094();
    uVar10 = param_3;
    uVar12 = param_4;
    uVar3 = FUN_001268ec();
    local_80 = local_80 - (long)(iVar2 << (ulong)(uVar3 & 0x1f));
    uVar11 = uVar11 + (uint)(iVar2 << (ulong)(uVar1 & 0x1f));
  }
  if (local_80 != 0) {
    FUN_00126070();
    uVar5 = FUN_001268c8();
    if ((uVar5 & 0xffffffff) <= local_80) {
      do {
        uVar12 = 0x1a8;
LAB_001259fc:
        FUN_00126020(uVar12);
        FUN_001260a0();
      } while( true );
    }
    if (local_d8 == 0) {
      FUN_00126070();
      FUN_00125f5c();
      auVar13 = thunk_FUN_00126114();
      local_d0 = uVar12;
      local_c8 = uVar10;
    }
    FUN_00126070();
    iVar2 = FUN_00126338();
    if (0 < iVar2) {
      FUN_00126154(param_5);
      lVar8 = thunk_FUN_00126114();
      FUN_001260bc(lVar8 + uVar4);
      FUN_00111154();
      uVar11 = local_80 + uVar11;
    }
  }
LAB_001259bc:
  if (auVar13._0_8_ != 0) {
    FUN_001184fc(auVar13._0_8_,auVar13._8_8_,local_c8,local_d0);
  }
  return uVar11;
}


