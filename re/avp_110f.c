// ===== 0x110f9c -> FUN_00110f50 @ 00110f50

void FUN_00110f50(long *param_1,ulong param_2,ulong param_3)

{
  bool bVar1;
  long lVar2;
  ulong uVar3;
  long *plVar4;
  ulong uVar5;
  
  lVar2 = (param_2 & 0xff) * 0x101010101010101;
  if (*DAT_00110ec0 == '\0') {
    if (param_3 == 0) {
      return;
    }
    if (((ulong)param_1 & 7) != 0) {
      uVar5 = 8 - ((ulong)param_1 & 7);
      uVar3 = param_3;
      if ((long)uVar5 <= (long)param_3) {
        uVar3 = uVar5;
      }
      for (; uVar3 != 0; uVar3 = uVar3 - 1) {
        *(char *)param_1 = (char)lVar2;
        param_3 = param_3 - 1;
        if (param_3 == 0) {
          return;
        }
        param_1 = (long *)((long)param_1 + 1);
      }
    }
  }
  else if (0x3f < param_3) {
    *param_1 = lVar2;
    param_1[1] = lVar2;
    plVar4 = (long *)((ulong)(param_1 + 2) & 0xfffffffffffffff0);
    uVar3 = (long)(param_3 + (long)param_1) - (long)(plVar4 + 8);
    if (plVar4 + 8 <= (long *)(param_3 + (long)param_1) && uVar3 != 0) {
      do {
        *plVar4 = lVar2;
        plVar4[1] = lVar2;
        plVar4[2] = lVar2;
        plVar4[3] = lVar2;
        plVar4[4] = lVar2;
        plVar4[5] = lVar2;
        plVar4[6] = lVar2;
        plVar4[7] = lVar2;
        plVar4 = plVar4 + 8;
        bVar1 = 0x3f < uVar3;
        uVar3 = uVar3 - 0x40;
      } while (bVar1 && uVar3 != 0);
    }
    plVar4 = (long *)((long)plVar4 + uVar3);
    *plVar4 = lVar2;
    plVar4[1] = lVar2;
    plVar4[2] = lVar2;
    plVar4[3] = lVar2;
    plVar4[4] = lVar2;
    plVar4[5] = lVar2;
    plVar4[6] = lVar2;
    plVar4[7] = lVar2;
    return;
  }
  while (7 < param_3) {
    *param_1 = lVar2;
    param_3 = param_3 - 8;
    param_1 = param_1 + 1;
  }
  for (; param_3 != 0; param_3 = param_3 - 1) {
    *(char *)param_1 = (char)lVar2;
    param_1 = (long *)((long)param_1 + 1);
  }
  return;
}


// ===== 0x110f28 -> FUN_00110ed0 @ 00110ed0

void FUN_00110ed0(undefined8 *param_1,ulong param_2)

{
  undefined8 *puVar1;
  bool bVar2;
  ulong uVar3;
  ulong uVar4;
  
  if (*DAT_00110ec0 == '\0') {
    if (param_2 == 0) {
      return;
    }
    if (((ulong)param_1 & 7) != 0) {
      uVar4 = 8 - ((ulong)param_1 & 7);
      uVar3 = param_2;
      if ((long)uVar4 <= (long)param_2) {
        uVar3 = uVar4;
      }
      for (; uVar3 != 0; uVar3 = uVar3 - 1) {
        *(undefined1 *)param_1 = 0;
        param_2 = param_2 - 1;
        if (param_2 == 0) {
          return;
        }
        param_1 = (undefined8 *)((long)param_1 + 1);
      }
    }
  }
  else if (0x7f < param_2) {
    *param_1 = 0;
    param_1[1] = 0;
    param_1[2] = 0;
    param_1[3] = 0;
    param_1[4] = 0;
    param_1[5] = 0;
    param_1[6] = 0;
    param_1[7] = 0;
    uVar3 = (ulong)(param_1 + 8) & 0xffffffffffffffc0;
    uVar4 = (long)(param_2 + (long)param_1) - (long)(uVar3 + 0x40);
    if ((undefined1 *)(uVar3 + 0x40) <= (undefined1 *)(param_2 + (long)param_1) && uVar4 != 0) {
      do {
        DC_ZVA(uVar3);
        uVar3 = uVar3 + 0x40;
        bVar2 = 0x3f < uVar4;
        uVar4 = uVar4 - 0x40;
      } while (bVar2 && uVar4 != 0);
    }
    puVar1 = (undefined8 *)(uVar3 + uVar4);
    *puVar1 = 0;
    puVar1[1] = 0;
    puVar1[2] = 0;
    puVar1[3] = 0;
    puVar1[4] = 0;
    puVar1[5] = 0;
    puVar1[6] = 0;
    puVar1[7] = 0;
    return;
  }
  while (7 < param_2) {
    *param_1 = 0;
    param_2 = param_2 - 8;
    param_1 = param_1 + 1;
  }
  for (; param_2 != 0; param_2 = param_2 - 1) {
    *(undefined1 *)param_1 = 0;
    param_1 = (undefined8 *)((long)param_1 + 1);
  }
  return;
}


// ===== 0x119cc8 -> FUN_00119be0 @ 00119be0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00119be0(ulong param_1,ulong param_2,ulong param_3,long param_4,ulong param_5)

{
  undefined1 uVar1;
  int iVar2;
  uint uVar3;
  long lVar4;
  undefined8 uVar5;
  undefined8 *puVar6;
  undefined8 *puVar7;
  long lVar8;
  long extraout_x8;
  ulong uVar9;
  undefined1 *extraout_x8_00;
  undefined1 *extraout_x8_01;
  ulong uVar10;
  ulong uVar11;
  undefined8 *puVar12;
  ulong uVar13;
  long unaff_x23;
  undefined1 auVar14 [16];
  
  auVar14._8_8_ = param_4;
  auVar14._0_8_ = param_4;
  if (param_2 <= param_1 && param_1 < param_3) {
    if (((*(long *)(param_1 + 0x4e8) != 0) || (*(long *)(param_1 + 0x4f0) != 0)) ||
       (*(long *)(param_1 + 0x480) == 0)) {
      uVar5 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
      FUN_00105548(uVar5,0x9b4);
    }
    lVar8 = param_4;
    uVar9 = param_5;
    FUN_001230a4();
    if (uVar9 == 0 && lVar8 == 0) {
      FUN_001232b8();
      puVar7 = (undefined8 *)(unaff_x23 + 0x28);
      auVar14 = FUN_00120dfc(unaff_x23 + 0x20,unaff_x23 + 0x20,puVar7,*(undefined1 *)(unaff_x23 + 3)
                             ,*(undefined8 *)(extraout_x8 + 0x80),
                             *(undefined8 *)(extraout_x8 + 0x88));
      if (auVar14._0_8_ == 0) {
        puVar7 = (undefined8 *)(unaff_x23 + 0x30);
        auVar14 = FUN_00120dfc(unaff_x23 + 0x28,unaff_x23 + 0x28,puVar7,
                               *(undefined1 *)(unaff_x23 + 2),_DAT_7003aa88,_DAT_7003aa90);
        if (auVar14._0_8_ == 0) {
          uVar5 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
          FUN_00105548(uVar5,0x3d9);
        }
      }
      param_5 = 0x4000;
    }
    else {
      if (((param_5 == 0) || ((param_5 & 0x3fff) != 0)) || (param_4 == 0)) {
        uVar5 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
        FUN_00105548(uVar5,0x9c1);
      }
      puVar7 = (undefined8 *)(param_4 + param_5);
    }
    puVar6 = auVar14._8_8_;
    uVar13 = auVar14._0_8_;
    uVar9 = 0;
    uVar10 = param_5 & 0xfffffffffffffff8;
    uVar11 = uVar13;
    do {
      puVar12 = (undefined8 *)(uVar11 + (uVar10 - 8));
      if (puVar12 < puVar6 || puVar7 <= puVar12) goto LAB_00119e74;
      *puVar12 = 0x7374616b7374616b;
      puVar12 = (undefined8 *)(uVar11 + (uVar10 - 0x10));
      if (puVar12 < puVar6) goto LAB_00119e74;
      *puVar12 = 0x7374616b7374616b;
      puVar12 = (undefined8 *)(uVar11 + (uVar10 - 0x18));
      if (puVar12 < puVar6) goto LAB_00119e74;
      *puVar12 = 0x7374616b7374616b;
      puVar12 = (undefined8 *)(uVar11 + (uVar10 - 0x20));
      if (puVar12 < puVar6) goto LAB_00119e74;
      *puVar12 = 0x7374616b7374616b;
      uVar9 = uVar9 + 0x20;
      uVar11 = uVar11 - 0x20;
    } while (uVar13 < uVar11 + uVar10);
    if (uVar10 != uVar9) {
      uVar5 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
      FUN_00105548(uVar5,0x9cf);
    }
    if (param_4 != 0) {
      FUN_00116504(param_4,param_5);
    }
    FUN_00123258();
    FUN_001230d0();
    iVar2 = FUN_0010e124();
    if (0 < iVar2) {
      uVar5 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
      FUN_00105548(uVar5,0x417);
    }
    FUN_00123258();
    FUN_001230d0();
    uVar3 = FUN_0010e240();
    uVar1 = 0x7f < uVar3;
    if ((bool)uVar1) {
      uVar5 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
      FUN_00105548(uVar5,0x41c);
    }
    FUN_001230d0();
    FUN_001190bc();
    FUN_00123088();
    FUN_00122ff0();
    if (!(bool)uVar1) {
      lVar8 = DAT_001424c8 + (ulong)(uVar3 << 0xf);
      *extraout_x8_00 = 1;
      FUN_001231a4(lVar8,uVar13,param_5);
      lVar4 = FUN_00116500();
      FUN_00123088();
      FUN_00122ff0();
      if (!(bool)uVar1) {
        *extraout_x8_01 = 0;
        if (lVar4 == lVar8) {
          *(long *)(param_1 + 0x4e8) = lVar8;
          *(ulong *)(param_1 + 0x4f0) = lVar8 + param_5;
          *(ulong *)(param_1 + 0x4e0) = uVar13;
          return;
        }
        uVar5 = FUN_00122eec();
                    /* WARNING: Subroutine does not return */
        FUN_00105548(uVar5,0x9e3);
      }
    }
  }
LAB_00119e74:
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


