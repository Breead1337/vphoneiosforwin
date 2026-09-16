// ===== 0x1285d4 -> FUN_001285d4 @ 001285d4

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001285d4(long *param_1,ulong param_2)

{
  code *pcVar1;
  int iVar2;
  undefined8 uVar3;
  uint local_3c;
  long local_38;
  
  local_38 = _DAT_7002add8;
  uVar3 = 6;
  if ((param_1 == (long *)0x0) || (param_2 == 0)) goto LAB_00128698;
  if (param_1[1] == 0 || *param_1 == 0) {
LAB_00128694:
    uVar3 = 0;
  }
  else {
    uVar3 = FUN_0012ae90(param_1,5,&DAT_001426b8,param_2,0xc0,0);
    if ((int)uVar3 != 0) goto LAB_00128698;
    if (param_2 + 0x10 < param_2) {
                    /* WARNING: Does not return */
      pcVar1 = (code *)SoftwareBreakpoint(0x5519,0x1286d0);
      (*pcVar1)();
    }
    iVar2 = FUN_0013c338(param_2,0x494d344d);
    if (iVar2 == 0) {
      local_3c = 0;
      uVar3 = FUN_0012abe4(param_2 + 0x10,&local_3c);
      if ((int)uVar3 != 0) goto LAB_00128698;
      if (local_3c < 3) goto LAB_00128694;
    }
    uVar3 = 2;
  }
LAB_00128698:
  if (_DAT_7002add8 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18(uVar3);
}


// ===== 0x1286d4 -> FUN_001286d4 @ 001286d4

undefined8 FUN_001286d4(long *param_1,undefined8 *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined8 uVar3;
  
  uVar3 = 0;
  if (param_1 != (long *)0x0) {
    if (param_2 == (undefined8 *)0x0) {
      uVar3 = 6;
    }
    else {
      param_2[1] = 0;
      *param_2 = 0;
      param_2[3] = 0;
      param_2[2] = 0;
      if (param_1[1] != 0 && *param_1 != 0) {
        uVar3 = FUN_0012ae90(param_1,2,&DAT_00142730,param_2,0x20,0);
        if ((int)uVar3 != 0) {
          return uVar3;
        }
        if (param_2 + 2 < param_2) {
                    /* WARNING: Does not return */
          pcVar1 = (code *)SoftwareBreakpoint(0x5519,0x12876c);
          (*pcVar1)();
        }
        iVar2 = FUN_0013c338(param_2,0x494d3452);
        if (iVar2 != 0) {
          return 2;
        }
      }
      uVar3 = 0;
    }
  }
  return uVar3;
}


// ===== 0x1284a0 -> FUN_001284a0 @ 001284a0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001284a0(long param_1,undefined8 *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined8 uVar3;
  long *plVar4;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 uStack_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  long local_28;
  
  local_28 = _DAT_7002add8;
  uVar3 = 6;
  if ((param_1 != 0) && (param_2 != (undefined8 *)0x0)) {
    uStack_48 = 0;
    local_50 = 0;
    uStack_38 = 0;
    uStack_40 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uVar3 = FUN_001282f4(param_1,&local_d0);
    if ((int)uVar3 == 0) {
      param_2[1] = uStack_c8;
      *param_2 = local_d0;
      param_2[3] = uStack_b8;
      param_2[2] = local_c0;
      param_2[5] = uStack_a8;
      param_2[4] = local_b0;
      param_2[7] = uStack_98;
      param_2[6] = local_a0;
      param_2[9] = uStack_88;
      param_2[8] = local_90;
      param_2[0xb] = uStack_78;
      param_2[10] = local_80;
    }
    else {
      uVar3 = FUN_0012ae90(param_1,6,&DAT_00142580,param_2,0x90,0);
      if ((int)uVar3 == 0) {
        if (param_2 + 2 < param_2) {
LAB_001285cc:
                    /* WARNING: Does not return */
          pcVar1 = (code *)SoftwareBreakpoint(0x5519,0x1285d0);
          (*pcVar1)();
        }
        iVar2 = FUN_0013c338(param_2,0x494d3450);
        if (iVar2 == 0) {
          plVar4 = param_2 + 10;
          if (*plVar4 != 0) {
            uStack_e8 = 0;
            local_f0 = 0;
            uStack_d8 = 0;
            uStack_e0 = 0;
            if (param_2 + 0xc < plVar4) goto LAB_001285cc;
            uVar3 = FUN_0013c3c4(plVar4,&local_f0);
            if ((int)uVar3 != 0) goto LAB_00128578;
          }
          uVar3 = 0;
        }
        else {
          uVar3 = 2;
        }
      }
    }
  }
LAB_00128578:
  if (_DAT_7002add8 != local_28) {
                    /* WARNING: Subroutine does not return */
    FUN_00123c18(uVar3);
  }
  return;
}


// ===== 0x1281cc -> FUN_001281cc @ 001281cc

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001281cc(ulong *param_1,ulong param_2)

{
  ulong uVar1;
  ulong uVar2;
  code *pcVar3;
  int iVar4;
  ulong uVar5;
  uint uVar6;
  long local_40;
  ulong local_38;
  ulong local_30;
  long local_28;
  
  local_28 = _DAT_7002add8;
  local_40 = 0;
  local_38 = 0;
  local_30 = 0;
  uVar5 = 6;
  if (((param_1 != (ulong *)0x0) && (param_2 != 0)) &&
     (uVar5 = FUN_0012a8b0(param_1,&local_40), (int)uVar5 == 0)) {
    if (local_40 == 0x2000000000000010) {
      uVar1 = *param_1;
      uVar2 = param_1[1];
      if ((uVar2 == 0) && (uVar1 != 0)) {
LAB_001282ec:
                    /* WARNING: Does not return */
        pcVar3 = (code *)SoftwareBreakpoint(0x5519,0x1282f0);
        (*pcVar3)();
      }
      if (CARRY8(uVar1,uVar2)) {
        uVar5 = 7;
      }
      else {
        if ((local_30 == 0) && (local_38 != 0)) goto LAB_001282ec;
        uVar5 = 7;
        if ((!CARRY8(local_38,local_30)) &&
           ((uVar1 + uVar2 == local_38 + local_30 &&
            (uVar5 = FUN_0012af5c(&local_38,4,&DAT_00142520,param_2,0x40,0), (int)uVar5 == 0)))) {
          if (param_2 + 0x10 < param_2) goto LAB_001282ec;
          iVar4 = FUN_0013c338(param_2,0x494d4734);
          uVar6 = 0;
          if (iVar4 != 0) {
            uVar6 = 2;
          }
          uVar5 = (ulong)uVar6;
        }
      }
    }
    else {
      uVar5 = 2;
    }
  }
  if (_DAT_7002add8 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18(uVar5);
}


