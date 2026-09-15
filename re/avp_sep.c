// ===== 0x10d450 -> FUN_0010d450 @ 0010d450

undefined8
FUN_0010d450(long *param_1,long *param_2,long *param_3,undefined8 param_4,ulong param_5,
            ulong param_6,ulong param_7,long param_8,long param_9,long param_10,long param_11,
            long param_12,long param_13,long *param_14,long *param_15,long *param_16,
            undefined8 param_17,long param_18,byte param_19)

{
  ulong uVar1;
  
  if ((param_1 == (long *)0x0) || (param_9 == 0)) {
    return 0xffffffff;
  }
  if (param_2 <= param_1 && param_1 < param_3) {
    *param_1 = param_9;
    param_1[2] = param_5;
    param_1[3] = param_6;
    param_1[4] = param_7;
    param_1[5] = param_8;
    param_1[8] = param_10;
    param_1[9] = param_11;
    param_1[10] = param_12;
    param_1[0xb] = param_13;
    if (param_15 <= param_14 && param_14 < param_16) {
      param_1[6] = *param_14;
      param_1[1] = param_18;
      if (param_6 <= param_5 && param_5 < param_7) {
        if (*(code **)(param_5 + 8) == (code *)0x0) {
                    /* WARNING: Subroutine does not return */
          FUN_0012e944(0xffffffff);
        }
        (**(code **)(param_5 + 8))(param_1,param_2,param_3);
        if ((param_19 & 1) == 0) {
          param_1[0x10] = 0;
          param_1[0x11] = 0;
          param_1[0xe] = 0;
          param_1[0xf] = 0;
          param_1[0xc] = 0;
        }
        else {
          FUN_00111968(param_1,param_2,param_3,param_4);
        }
        uVar1 = param_1[8];
        if ((ulong)param_1[9] <= uVar1 && uVar1 < (ulong)param_1[10]) {
          if (*(uint *)(uVar1 + 0x10) != 0) {
            *(undefined4 *)(*param_1 + (ulong)*(uint *)(uVar1 + 0x10)) = 0x1111;
            return 0;
          }
          return 0;
        }
      }
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x1066ac -> FUN_00106674 @ 00106674

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00106674(undefined8 param_1,undefined8 param_2,ulong param_3)

{
  undefined8 uVar1;
  undefined1 uVar2;
  bool bVar3;
  ulong uVar4;
  undefined1 auVar5 [16];
  
  FUN_00106af0();
  uVar1 = _DAT_7002add8;
  auVar5 = FUN_00106bc4();
  uVar4 = auVar5._0_8_;
  bVar3 = auVar5._8_8_ <= uVar4;
  uVar2 = bVar3 && uVar4 == param_3;
  if (!bVar3 || param_3 <= uVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  FUN_0010d450();
  FUN_00106b20(uVar1);
  if ((bool)uVar2) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


// ===== 0x106570 -> FUN_001063dc @ 001063dc

undefined8 FUN_001063dc(undefined8 param_1,ulong param_2,long *param_3)

{
  uint uVar1;
  long *plVar2;
  ulong uVar3;
  ulong *puVar4;
  long *plVar5;
  uint *puVar6;
  undefined8 uVar7;
  undefined4 *puVar8;
  undefined1 auVar9 [16];
  
  auVar9 = FUN_00106bc4();
  plVar2 = auVar9._0_8_;
  if (plVar2 < auVar9._8_8_ || param_3 <= plVar2) goto LAB_0010663c;
  if ((((short)plVar2[0x28] != 0x101) && ((short)plVar2[0x28] != 0x200)) || (*plVar2 == 0))
  goto LAB_00106638;
  if ((*(byte *)((long)plVar2 + 0x143) & 1) == 0) {
    FUN_001061e4(param_1);
    uVar3 = FUN_001031d0(param_2);
    if (uVar3 != 0) {
      param_2 = uVar3;
    }
    if ((*(ushort *)(plVar2 + 0x28) & 0x60) != 0) {
      if ((param_2 & 0xfffffff0000007ff) != 0) goto LAB_00106638;
      puVar4 = (ulong *)FUN_00106640(param_1);
      if ((*puVar4 & 1) == 0) {
        puVar4 = (ulong *)FUN_00106640(param_1);
        *puVar4 = param_2;
      }
      else if (param_2 != (*puVar4 & 0xffffff800)) goto LAB_00106638;
    }
    if (*(char *)((long)plVar2 + 0x142) == '\x01') {
      if (0xf < *(ushort *)(plVar2 + 0x28)) {
LAB_00106638:
                    /* WARNING: Subroutine does not return */
        FUN_0010550c();
      }
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar6 = (uint *)FUN_00106748(param_1,(int)plVar5[0x2f]);
      uVar1 = *puVar6;
      FUN_001185a8();
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar6 = (uint *)FUN_00106748(param_1,(int)plVar5[0x2f]);
      *puVar6 = uVar1 & 0xfffffffd;
      uVar7 = thunk_FUN_00100370();
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar8 = (undefined4 *)FUN_00106748(param_1,*(undefined4 *)((long)plVar5 + 0x17c));
      *puVar8 = (int)uVar7;
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar8 = (undefined4 *)FUN_00106748(param_1,(int)plVar5[0x30]);
      *puVar8 = (int)((ulong)uVar7 >> 0x20);
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar6 = (uint *)FUN_00106748(param_1,(int)plVar5[0x2f]);
      *puVar6 = uVar1 | 2;
      FUN_00118654();
    }
  }
  if (*(char *)((long)plVar2 + 0x145) == '\x01') {
    param_3 = plVar2 + 0xd;
    FUN_00106674(param_1,plVar2 + 0xd,param_3,plVar2 + 0x1f,0x70028a00,0);
  }
  if ((*(byte *)((long)plVar2 + 0x143) & 1) == 0) {
    auVar9 = FUN_00106bc4(param_1);
    plVar5 = auVar9._0_8_;
    if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) {
LAB_0010663c:
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    puVar8 = (undefined4 *)FUN_00106748(param_1,*(undefined4 *)((long)plVar5 + 0x174));
    *puVar8 = 0x10;
    if (plVar2[2] != 0) {
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar8 = (undefined4 *)FUN_00106788(param_1,*(undefined4 *)((long)plVar5 + 0x174));
      *puVar8 = 0x10;
    }
  }
  if (*(char *)((long)plVar2 + 0x145) == '\x01') {
    FUN_001067c8(plVar2 + 0xd,plVar2 + 0xd,plVar2 + 0x1f,0x70028a00,1);
  }
  return 0;
}


// ===== 0x1063dc -> FUN_001063dc @ 001063dc

undefined8 FUN_001063dc(undefined8 param_1,ulong param_2,long *param_3)

{
  uint uVar1;
  long *plVar2;
  ulong uVar3;
  ulong *puVar4;
  long *plVar5;
  uint *puVar6;
  undefined8 uVar7;
  undefined4 *puVar8;
  undefined1 auVar9 [16];
  
  auVar9 = FUN_00106bc4();
  plVar2 = auVar9._0_8_;
  if (plVar2 < auVar9._8_8_ || param_3 <= plVar2) goto LAB_0010663c;
  if ((((short)plVar2[0x28] != 0x101) && ((short)plVar2[0x28] != 0x200)) || (*plVar2 == 0))
  goto LAB_00106638;
  if ((*(byte *)((long)plVar2 + 0x143) & 1) == 0) {
    FUN_001061e4(param_1);
    uVar3 = FUN_001031d0(param_2);
    if (uVar3 != 0) {
      param_2 = uVar3;
    }
    if ((*(ushort *)(plVar2 + 0x28) & 0x60) != 0) {
      if ((param_2 & 0xfffffff0000007ff) != 0) goto LAB_00106638;
      puVar4 = (ulong *)FUN_00106640(param_1);
      if ((*puVar4 & 1) == 0) {
        puVar4 = (ulong *)FUN_00106640(param_1);
        *puVar4 = param_2;
      }
      else if (param_2 != (*puVar4 & 0xffffff800)) goto LAB_00106638;
    }
    if (*(char *)((long)plVar2 + 0x142) == '\x01') {
      if (0xf < *(ushort *)(plVar2 + 0x28)) {
LAB_00106638:
                    /* WARNING: Subroutine does not return */
        FUN_0010550c();
      }
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar6 = (uint *)FUN_00106748(param_1,(int)plVar5[0x2f]);
      uVar1 = *puVar6;
      FUN_001185a8();
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar6 = (uint *)FUN_00106748(param_1,(int)plVar5[0x2f]);
      *puVar6 = uVar1 & 0xfffffffd;
      uVar7 = thunk_FUN_00100370();
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar8 = (undefined4 *)FUN_00106748(param_1,*(undefined4 *)((long)plVar5 + 0x17c));
      *puVar8 = (int)uVar7;
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar8 = (undefined4 *)FUN_00106748(param_1,(int)plVar5[0x30]);
      *puVar8 = (int)((ulong)uVar7 >> 0x20);
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar6 = (uint *)FUN_00106748(param_1,(int)plVar5[0x2f]);
      *puVar6 = uVar1 | 2;
      FUN_00118654();
    }
  }
  if (*(char *)((long)plVar2 + 0x145) == '\x01') {
    param_3 = plVar2 + 0xd;
    FUN_00106674(param_1,plVar2 + 0xd,param_3,plVar2 + 0x1f,0x70028a00,0);
  }
  if ((*(byte *)((long)plVar2 + 0x143) & 1) == 0) {
    auVar9 = FUN_00106bc4(param_1);
    plVar5 = auVar9._0_8_;
    if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) {
LAB_0010663c:
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    puVar8 = (undefined4 *)FUN_00106748(param_1,*(undefined4 *)((long)plVar5 + 0x174));
    *puVar8 = 0x10;
    if (plVar2[2] != 0) {
      auVar9 = FUN_00106bc4(param_1);
      plVar5 = auVar9._0_8_;
      if (plVar5 < auVar9._8_8_ || param_3 <= plVar5) goto LAB_0010663c;
      puVar8 = (undefined4 *)FUN_00106788(param_1,*(undefined4 *)((long)plVar5 + 0x174));
      *puVar8 = 0x10;
    }
  }
  if (*(char *)((long)plVar2 + 0x145) == '\x01') {
    FUN_001067c8(plVar2 + 0xd,plVar2 + 0xd,plVar2 + 0x1f,0x70028a00,1);
  }
  return 0;
}


