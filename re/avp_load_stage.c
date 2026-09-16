// ===== 0x00107568 -> FUN_00107568 @ 00107568

void FUN_00107568(uint *param_1,uint *param_2,uint *param_3,undefined8 param_4,uint *param_5,
                 uint *param_6,uint *param_7,undefined8 param_8,uint param_9,undefined4 *param_10,
                 undefined4 *param_11,undefined4 *param_12,undefined8 param_13,undefined8 param_14,
                 undefined8 param_15,undefined8 param_16,undefined8 param_17,ulong param_18,
                 undefined8 *param_19,undefined8 *param_20,undefined8 *param_21,undefined8 param_22,
                 undefined8 param_23,undefined8 param_24,undefined8 param_25,undefined8 param_26,
                 undefined8 param_27,undefined8 param_28)

{
  undefined4 uVar1;
  undefined1 in_ZR;
  int iVar2;
  undefined8 uVar3;
  ulong extraout_x1;
  ulong uVar4;
  uint *puVar5;
  undefined8 extraout_x8;
  int iVar6;
  undefined4 local_74;
  undefined8 local_70 [2];
  
  puVar5 = param_5;
  FUN_00107974(param_1,0);
  local_74 = 0;
  uVar4 = extraout_x1;
  if ((puVar5 != (uint *)0x0) && (in_ZR = 0, param_9 == 1)) {
    in_ZR = param_5 >= param_6 && param_5 == param_7;
    if (param_5 < param_6 || param_7 <= param_5) goto LAB_001077bc;
    uVar4 = (ulong)*param_5;
  }
  local_70[0] = extraout_x8;
  FUN_00127704(0x3000c,uVar4);
  iVar6 = (int)param_7;
  if (param_1 == (uint *)0x0) {
    uVar1 = 0x40030004;
LAB_0010762c:
    FUN_001275ac(uVar1);
    uVar3 = 0xffffffff;
LAB_00107634:
    iVar2 = FUN_00107984(uVar3);
joined_r0x001076e0:
    if (param_10 != (undefined4 *)0x0) {
      in_ZR = param_10 >= param_11 && param_10 == param_12;
      if (param_10 < param_11 || param_12 <= param_10) goto LAB_001077bc;
      *param_10 = local_74;
    }
    if (iVar2 == 0) {
      FUN_00127704(0x3000d,local_74);
      uVar3 = 0;
      goto LAB_0010769c;
    }
  }
  else {
    if (param_1 < param_2 || param_3 <= param_1) goto LAB_001077bc;
    in_ZR = param_18 == *param_1;
    if (param_18 < *param_1) {
      uVar1 = 0x40030001;
      goto LAB_0010762c;
    }
    if ((param_5 == (uint *)0x0) && (param_9 != 0)) {
      FUN_00107984();
      FUN_001275ac(iVar6 + 1);
LAB_001076dc:
      iVar2 = -1;
      goto joined_r0x001076e0;
    }
    in_ZR = param_9 == 2;
    if ((param_9 < 2) || (param_10 != (undefined4 *)0x0)) {
      in_ZR = param_1[2] == 0x4d656d7a;
      if ((!(bool)in_ZR) && (in_ZR = param_1[2] == 0x696d6734, !(bool)in_ZR)) {
        FUN_00107984();
        FUN_00127704(iVar6 + 7);
        goto LAB_001076dc;
      }
      uVar3 = FUN_001011a8(param_1,param_2,param_3,param_4,param_5,param_6,param_7,param_8,param_9,
                           &local_74,&local_74,local_70,&PTR_LOOP_0013ce48,param_14,param_15,
                           param_16,param_17,param_18,param_19,param_20,param_21,param_22,param_23,
                           param_24,param_25,param_26,param_27,param_28);
      goto LAB_00107634;
    }
    FUN_00107984();
    FUN_001275ac(iVar6 + 2);
  }
  FUN_00127704(iVar6 + 0xd,local_74);
  if (param_19 != (undefined8 *)0x0) {
    in_ZR = param_19 >= param_20 && param_19 == param_21;
    if (param_19 < param_20 || param_21 <= param_19) {
LAB_001077bc:
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    *param_19 = 0;
  }
  uVar3 = 0xffffffff;
LAB_0010769c:
  FUN_00107960(local_70[0],uVar3);
  if ((bool)in_ZR) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


