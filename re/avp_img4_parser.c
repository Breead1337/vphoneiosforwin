// ===== 0x129318 -> FUN_00129318 @ 00129318

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00129318(long param_1,undefined8 param_2,undefined8 *param_3)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  code *pcVar3;
  undefined8 uVar4;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  long local_48;
  undefined8 uStack_40;
  long local_38;
  
  local_38 = _DAT_7002add8;
  uVar4 = 6;
  if ((param_1 != 0) && (param_3 != (undefined8 *)0x0)) {
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    param_3[1] = 0;
    *param_3 = 0;
    param_3[3] = 0;
    param_3[2] = 0;
    param_3[5] = 0;
    param_3[4] = 0;
    param_3[7] = 0;
    param_3[6] = 0;
    param_3[9] = 0;
    param_3[8] = 0;
    param_3[0xb] = 0;
    param_3[10] = 0;
    param_3[0xd] = 0;
    param_3[0xc] = 0;
    param_3[0xf] = 0;
    param_3[0xe] = 0;
    param_3[0x11] = 0;
    param_3[0x10] = 0;
    param_3[0x13] = 0;
    param_3[0x12] = 0;
    param_3[0x15] = 0;
    param_3[0x14] = 0;
    param_3[0x17] = 0;
    param_3[0x16] = 0;
    param_3[0x19] = 0;
    param_3[0x18] = 0;
    param_3[0x1b] = 0;
    param_3[0x1a] = 0;
    param_3[0x1d] = 0;
    param_3[0x1c] = 0;
    param_3[0x1f] = 0;
    param_3[0x1e] = 0;
    param_3[0x21] = 0;
    param_3[0x20] = 0;
    param_3[0x23] = 0;
    param_3[0x22] = 0;
    param_3[0x25] = 0;
    param_3[0x24] = 0;
    param_3[0x27] = 0;
    param_3[0x26] = 0;
    param_3[0x29] = 0;
    param_3[0x28] = 0;
    param_3[0x2b] = 0;
    param_3[0x2a] = 0;
    param_3[0x2d] = 0;
    param_3[0x2c] = 0;
    param_3[0x2f] = 0;
    param_3[0x2e] = 0;
    param_3[0x31] = 0;
    param_3[0x30] = 0;
    param_3[0x33] = 0;
    param_3[0x32] = 0;
    param_3[0x35] = 0;
    param_3[0x34] = 0;
    param_3[0x37] = 0;
    param_3[0x36] = 0;
    param_3[0x38] = 0;
    local_48 = param_1;
    uStack_40 = param_2;
    uVar4 = FUN_001281cc(&local_48,&local_90);
    if ((int)uVar4 == 0) {
      puVar1 = param_3 + 0x1d;
      if (puVar1 < param_3 + 0xb) {
LAB_00129440:
                    /* WARNING: Does not return */
        pcVar3 = (code *)SoftwareBreakpoint(0x5519,0x129444);
        (*pcVar3)();
      }
      uVar4 = FUN_001284a0(&local_80);
      if ((int)uVar4 == 0) {
        puVar2 = param_3 + 0x35;
        if (puVar2 < puVar1) goto LAB_00129440;
        uVar4 = FUN_001285d4(&local_70,puVar1);
        if ((int)uVar4 == 0) {
          if (param_3 + 0x39 < puVar2) goto LAB_00129440;
          uVar4 = FUN_001286d4(&uStack_60,puVar2);
          if ((int)uVar4 == 0) {
            param_3[2] = uStack_78;
            param_3[1] = local_80;
            param_3[4] = uStack_68;
            param_3[3] = local_70;
          }
        }
      }
    }
  }
  if (_DAT_7002add8 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18(uVar4);
}


// ===== 0x128b5c -> FUN_00128b5c @ 00128b5c

void FUN_00128b5c(long param_1,undefined4 *param_2)

{
  int iVar1;
  
  iVar1 = 6;
  if ((param_1 != 0) && (param_2 != (undefined4 *)0x0)) {
    if (*(long *)(param_1 + 0x90) == 0 || *(long *)(param_1 + 0x88) == 0) {
      iVar1 = 1;
    }
    else {
      iVar1 = FUN_0012abe4(param_1 + 0x68,param_2);
    }
  }
  if ((param_2 != (undefined4 *)0x0) && (iVar1 != 0)) {
    *param_2 = 0;
  }
  return;
}


// ===== 0x128e6c -> FUN_00128e6c @ 00128e6c

undefined8 FUN_00128e6c(long param_1,long param_2)

{
  undefined8 uVar1;
  
  uVar1 = 6;
  if ((param_1 != 0) && (param_2 != 0)) {
    uVar1 = 0;
    *(bool *)param_2 = *(long *)(param_1 + 0x18) != 0;
  }
  return uVar1;
}


