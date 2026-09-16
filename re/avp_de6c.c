// ===== 0x10de6c -> FUN_0010dd5c @ 0010dd5c

void FUN_0010dd5c(long *param_1,long *param_2,long *param_3,undefined8 param_4,ulong param_5)

{
  long *plVar1;
  long *plVar2;
  long *plVar3;
  undefined8 *puVar4;
  int iVar5;
  undefined8 uVar6;
  ulong extraout_x8;
  ulong uVar7;
  long lVar8;
  long lVar9;
  
  if (param_2 <= param_1 && param_1 < param_3) {
    plVar1 = param_1 + 2;
    plVar2 = plVar1 + (ulong)*(byte *)((long)param_1 + 0xd) * 5;
    if (!CARRY8((ulong)plVar1,(ulong)*(byte *)((long)param_1 + 0xd) * 0x28)) {
      if (plVar2 < plVar1 || param_1 + 0xc <= plVar2) goto LAB_0010dea8;
      FUN_0010df10();
      lVar9 = 0;
      do {
        if ((ulong)(*(uint *)(plVar2 + 4) & ((int)*(uint *)(plVar2 + 4) >> 0x1f ^ 0xffffffffU)) *
            0x10 + 0x10 == lVar9 + 0x10) break;
        uVar7 = *plVar2 + lVar9;
        if (uVar7 < (ulong)plVar2[1] || (ulong)plVar2[2] <= uVar7) goto LAB_0010dea8;
        lVar9 = lVar9 + 0x10;
      } while ((*(ushort *)(uVar7 + 0xe) & 1) != 0);
      lVar8 = 0;
      lVar9 = 0;
      uVar7 = extraout_x8;
      while (plVar3 = plVar1 + uVar7 * 5, !CARRY8((ulong)plVar1,uVar7 * 0x28)) {
        if (plVar3 < plVar1 || param_1 + 0xc <= plVar3) goto LAB_0010dea8;
        if ((int)plVar3[4] <= lVar9) {
          thunk_FUN_001003f0();
          uVar6 = FUN_001031d0(*plVar2);
          *(undefined8 *)(*param_1 + 0x408) = uVar6;
          if ((param_5 & 1) != 0) {
            thunk_FUN_001003f0();
            do {
              FUN_0010dee4();
              iVar5 = FUN_0010dac0();
            } while (iVar5 == 0);
          }
          *(undefined4 *)(plVar2 + 4) = 0;
          return;
        }
        puVar4 = (undefined8 *)(*plVar2 + lVar8);
        if (puVar4 < (undefined8 *)plVar2[1] || (undefined8 *)plVar2[2] <= puVar4)
        goto LAB_0010dea8;
        uVar6 = FUN_001031d0(*puVar4);
        *puVar4 = uVar6;
        lVar9 = lVar9 + 1;
        lVar8 = lVar8 + 0x10;
        uVar7 = (ulong)*(byte *)((long)param_1 + 0xd);
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_0012e910();
  }
LAB_0010dea8:
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


