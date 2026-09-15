// ===== 0x106b48 -> FUN_00106b48 @ 00106b48

undefined1  [16] FUN_00106b48(uint param_1)

{
  ulong uVar1;
  undefined8 uVar2;
  ulong uVar3;
  undefined1 auVar4 [16];
  
  if ((param_1 & 0xffff) < 3) {
    uVar3 = (ulong)((param_1 & 0xffff) * 0x1a0);
    uVar2 = 0x70028a30;
    uVar1 = uVar3 + 0x70028a30;
    if (0xffffffff8ffd75cf < uVar3) {
                    /* WARNING: Subroutine does not return */
      FUN_0012e910();
    }
    if (uVar1 < 0x70028a30 || 0x70028f0f < uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    if (*(short *)(uVar3 + 0x70028b70) != 0) goto LAB_00106bb4;
  }
  uVar2 = 0;
  uVar1 = 0;
LAB_00106bb4:
  auVar4._8_8_ = uVar2;
  auVar4._0_8_ = uVar1;
  return auVar4;
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


// ===== 0x106640 -> FUN_00106640 @ 00106640

long FUN_00106640(undefined2 param_1,undefined8 param_2,ulong param_3)

{
  ulong uVar1;
  undefined1 auVar2 [16];
  
  auVar2 = FUN_00106bc4(param_1);
  uVar1 = auVar2._0_8_;
  if (auVar2._8_8_ <= uVar1 && uVar1 < param_3) {
    return *(long *)(uVar1 + 0x18) + 0x50000;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


// ===== 0x106748 -> FUN_00106748 @ 00106748

long FUN_00106748(undefined2 param_1,long param_2,long *param_3)

{
  long *plVar1;
  undefined1 auVar2 [16];
  
  auVar2 = FUN_00106bc4(param_1);
  plVar1 = auVar2._0_8_;
  if (auVar2._8_8_ <= plVar1 && plVar1 < param_3) {
    return *plVar1 + param_2;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


