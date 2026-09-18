// ===== 0x700759f0 -> FUN_700759f0 @ 700759f0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_700759f0(void)

{
  undefined8 uVar1;
  bool bVar2;
  ulong uVar3;
  ulong *extraout_x9;
  ulong *puVar4;
  ulong *extraout_x10;
  ulong *puVar5;
  ulong *extraout_x11;
  ulong *puVar6;
  ulong uVar7;
  ulong uVar8;
  ulong uVar9;
  ulong unaff_x23;
  undefined1 auVar10 [16];
  
  uVar1 = _DAT_7012a010;
  FUN_700769ec(&PTR_LAB_7011d018);
  puVar4 = extraout_x9;
  puVar5 = extraout_x10;
  puVar6 = extraout_x11;
  while( true ) {
    uVar7 = *puVar4;
    bVar2 = uVar7 == unaff_x23;
    if (bVar2) {
      FUN_70076764(uVar1);
      if (bVar2) {
        return;
      }
                    /* WARNING: Subroutine does not return */
      FUN_700dca28();
    }
    uVar8 = *puVar6;
    uVar9 = *puVar5;
    uVar3 = uVar8;
    auVar10 = FUN_70076730(uVar7,uVar9);
    if ((auVar10._0_8_ < auVar10._8_8_ || uVar3 <= auVar10._0_8_) ||
       (FUN_700b2780(s_image__p__bdev__p_type__c_c_c_c_o_70110d2b), uVar7 < uVar9 || uVar8 <= uVar7)
       ) break;
    puVar4 = (ulong *)(uVar7 + 0x20);
    puVar5 = (ulong *)(uVar7 + 0x28);
    puVar6 = (ulong *)(uVar7 + 0x30);
  }
                    /* WARNING: Subroutine does not return */
  FUN_700f03f0();
}


