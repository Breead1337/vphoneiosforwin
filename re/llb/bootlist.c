// ===== 0x70070084 -> FUN_70070084 @ 70070084

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_70070084(ulong param_1,long *param_2,long *param_3,code *param_4)

{
  long *plVar1;
  bool bVar2;
  code *pcVar3;
  int iVar4;
  int iVar5;
  ulong uVar6;
  ulong uVar7;
  long lVar8;
  long lVar9;
  char *pcVar10;
  undefined1 *puVar11;
  char *pcVar12;
  char *pcVar13;
  long lVar14;
  undefined1 *puVar15;
  ulong unaff_x30;
  undefined1 auVar16 [16];
  undefined8 uVar17;
  undefined4 uVar18;
  
  puVar11 = &LAB_70105fb8;
  uVar6 = FUN_700ad890(s_upgrade_retry_7011026e,s_upgrade_retry_7011026e,s_auto_boot_7011027c,
                       &LAB_70105fb8,0);
  pcVar10 = s_recover_70110286;
  uVar7 = FUN_700ad890(s_auto_boot_7011027c,s_auto_boot_7011027c,s_recover_70110286,&LAB_70105fb8,0)
  ;
  auVar16 = FUN_700a91e8();
  lVar14 = auVar16._0_8_;
  puVar15 = (undefined1 *)0x0;
  bVar2 = true;
  pcVar12 = (char *)0x0;
  pcVar13 = (char *)0x0;
  if (((uVar7 & 1) != 0) && ((uVar6 & 1) != 0)) {
    iVar4 = FUN_70083c20();
    if ((iVar4 == 0) || (iVar4 = FUN_700a92a4(), iVar4 == 0)) {
      puVar15 = (undefined1 *)0x0;
      pcVar12 = (char *)0x0;
      pcVar13 = (char *)0x0;
      bVar2 = true;
    }
    else {
      puVar15 = &LAB_70105fb8;
      FUN_700ae264(s_upgrade_retry_7011026e,s_upgrade_retry_7011026e,s_auto_boot_7011027c,
                   &LAB_70105fb8);
      bVar2 = false;
      pcVar13 = s_recover_70110286;
      pcVar12 = s_bootdelay_7011028e;
    }
  }
  _DAT_701288f8 = FUN_700e7d90();
  iVar4 = FUN_700ad804(s_bootdelay_7011028e,s_bootdelay_7011028e,s_boot_command_70110298,
                       &LAB_70105fb8,1);
  if ((uVar7 & 1) != 0) {
    uVar17 = 0x3974bfd3d441da3;
    FUN_70070434();
    lVar8 = FUN_700e7d90();
    while (iVar5 = FUN_7008999c(), iVar5 != 0xd && iVar5 != 10) {
      lVar9 = FUN_700e7d90();
      if ((ulong)(uint)(iVar4 * 1000000) < (ulong)(lVar9 - lVar8)) {
        _DAT_70128900 = FUN_700e7d90();
        uVar6 = 0;
        goto LAB_70070268;
      }
      FUN_700dc88c(10000);
    }
    FUN_700b2780(s_aborting_autoboot_due_to_user_in_701102a5);
  }
  goto LAB_70070224;
  while( true ) {
    if (lVar14 == 0) {
      lVar14 = 0;
      goto joined_r0x70070368;
    }
    FUN_700703f0();
    iVar4 = FUN_700b4550();
    uVar18 = (undefined4)((ulong)uVar17 >> 0x20);
    uVar6 = uVar6 + 0x38;
    if (iVar4 == 0) break;
LAB_70070268:
    plVar1 = (long *)(param_1 + uVar6);
    uVar7 = -(ulong)CARRY8(param_1,uVar6);
    if ((uVar7 != CARRY8(param_1,uVar6)) || ((long)uVar7 < 0)) {
                    /* WARNING: Subroutine does not return */
      FUN_700f0284();
    }
    if (plVar1 < param_2 || param_3 <= plVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_700f03f0();
    }
    if (*plVar1 == 0) {
      if (lVar14 == 0) {
        lVar14 = 0;
      }
      else {
        FUN_70070434();
      }
joined_r0x70070368:
      if (param_4 != (code *)0x0) {
        FUN_70070434();
        iVar4 = FUN_700a9418();
        if (iVar4 != 0) {
          FUN_700d11c8(lVar14,auVar16._8_8_,pcVar10,puVar11);
          FUN_70070470();
        }
        (*param_4)();
      }
      goto LAB_70070224;
    }
  }
  FUN_700e7220(0x20028,(char)plVar1[6]);
  uVar6 = FUN_700a93e8();
  if (((uVar6 & 1) == 0) && (uVar6 = FUN_700a9364(), (uVar6 & 1) == 0)) {
    FUN_700897f4();
  }
  iVar4 = FUN_700a9418();
  if (iVar4 != 0) {
    FUN_700703f0();
    FUN_700d11c8();
    FUN_70070470();
  }
  if (!bVar2) {
    FUN_700add9c(s_boot_command_70110298,s_boot_command_70110298,
                 s_aborting_autoboot_due_to_user_in_701102a5,&LAB_70105fb8,pcVar13,pcVar13,pcVar12,
                 puVar15,CONCAT44(uVar18,1));
    FUN_700ae318();
  }
  if ((code *)plVar1[4] == (code *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_700f02b8();
  }
  (*(code *)plVar1[4])();
LAB_70070224:
  FUN_700703f0();
  if (((unaff_x30 ^ unaff_x30 << 1) >> 0x3e & 1) != 0) {
                    /* WARNING: Does not return */
    pcVar3 = (code *)SoftwareBreakpoint(0xc471,0x70070254);
    (*pcVar3)();
  }
  FUN_700d11c8();
  return;
}


// ===== 0x7006c994 -> FUN_7006c994 @ 7006c994

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_7006c994(void)

{
  undefined1 in_ZR;
  int iVar1;
  int iVar2;
  undefined8 uVar3;
  ulong uVar4;
  undefined8 uVar5;
  long lVar6;
  undefined8 uVar7;
  long lVar8;
  undefined8 in_x3;
  undefined8 extraout_x8;
  undefined1 auVar9 [16];
  undefined1 auVar10 [16];
  undefined1 local_288 [16];
  long local_278;
  undefined8 uStack_270;
  undefined1 *local_268;
  undefined1 *puStack_260;
  undefined8 *local_258;
  undefined1 *local_250;
  undefined1 local_248 [16];
  undefined8 local_238;
  undefined8 uStack_230;
  undefined8 local_228;
  undefined8 local_220;
  undefined8 local_218;
  undefined1 auStack_210 [512];
  undefined8 local_10 [2];
  
  uVar3 = FUN_7006e334();
  FUN_7006e198();
  local_220 = 0;
  local_218 = 0;
  local_228 = 0;
  local_10[0] = extraout_x8;
  FUN_700b4ef0(auStack_210,0x200);
  FUN_700e70c8(0x20012);
  FUN_700ddb6c();
  uVar4 = FUN_7006e314();
  if ((uVar4 & 1) == 0) {
    iVar1 = FUN_700c7864();
    in_ZR = iVar1 - 0x13U == 2;
    if (iVar1 - 0x13U < 2) {
      FUN_700ddb78();
      FUN_700e70c8(0x1c000c);
    }
    else {
      iVar2 = FUN_700c78b0();
      if (iVar2 != 0) {
        FUN_7006e148(0x86d);
        uVar4 = (ulong)(uint)-iVar1;
        uVar7 = FUN_700c7864();
        FUN_700e7220(0x401c000d,uVar7);
        in_x3 = 0;
        uVar7 = 0;
        auVar9 = ZEXT816(0);
        goto LAB_7006cc94;
      }
    }
  }
  uVar5 = FUN_700ee210(0);
  uVar7 = 0x200;
  FUN_700ee1bc(uVar5,1);
  auVar9 = FUN_7006e130();
  uVar5 = in_x3;
  FUN_7006e1f8();
  iVar1 = FUN_700846c4(auStack_210,auStack_210,local_10);
  if (iVar1 < 0) {
    uVar4 = 0xffffffff;
  }
  else {
    lVar6 = FUN_7006e1f8(s_boot_path_7011008a);
    lVar8 = lVar6 + 10;
    auVar10 = FUN_700ad6e0(lVar6,lVar6);
    if (auVar10._0_8_ == 0) {
      uVar4 = 0xffffffff;
    }
    else {
      FUN_700c1d50(0x3c4d6673,0);
      iVar1 = FUN_7006d3e8();
      if (iVar1 < 0) {
        FUN_7006e148(0x889);
        uVar4 = 0xffffffff;
      }
      else {
        FUN_700c1d50(0x3e4d6673,0);
        uVar4 = FUN_7006d908();
        if (-1 < (int)uVar4) {
          local_268 = auStack_210;
          local_250 = &LAB_70105fb8;
          local_278 = lVar8;
          uStack_270 = uVar5;
          puStack_260 = local_268;
          local_258 = local_10;
          local_238 = uVar7;
          uStack_230 = in_x3;
          local_288 = auVar10;
          local_248 = auVar9;
          FUN_7006e1d4(local_288);
          FUN_700b27ac(local_248,0x200);
          FUN_700c1d50(0x3c4c4b46,0);
          uVar4 = FUN_700796d8(auVar9._0_8_,auVar9._8_8_,uVar7,in_x3,0x6b726e6c,&DAT_70120d88,
                               &DAT_70120d88,0x70120e38,&LAB_701063c8,&local_218,&local_218,
                               auStack_210,&LAB_70105fd0,&local_220,&local_220,&local_218,
                               &LAB_70105fd0,&local_228,&local_228,&local_220,&LAB_70105fd0);
          if ((int)uVar4 < 0) {
            FUN_7006e314();
          }
          else {
            FUN_700c1d50(0x3e4c4b46,0);
            in_ZR = DAT_70120d88 == '\x01';
            if (((bool)in_ZR) && (_DAT_70120dc0 != 0)) {
              FUN_7006e244();
              FUN_7006e188(0);
              FUN_700c6048();
              FUN_7006e260();
            }
            FUN_7008b0b0(1);
            FUN_70084fb4();
            FUN_7006e1f8();
            FUN_7006e234();
            FUN_700801b4();
            uVar4 = FUN_700830c4(0);
            if (-1 < (int)uVar4) {
              FUN_700844c4();
              uVar4 = FUN_7006cdd8(local_218,local_228,&DAT_70120d88,&DAT_70120d88,0x70120e38,
                                   &LAB_701063c8);
            }
          }
          goto LAB_7006cc94;
        }
      }
      FUN_7006e314();
    }
  }
LAB_7006cc94:
  FUN_700e7544(s_boot_breadcrumbs_7010ff8c,s_boot_breadcrumbs_7010ff8c,s_filesize_7010ff9d,
               &LAB_70105fb8);
  FUN_700d11c8(auVar9._0_8_,auVar9._8_8_,uVar7,in_x3);
  FUN_7006e234();
  FUN_700e5614();
  FUN_7006e174(local_10[0]);
  if (!(bool)in_ZR) {
                    /* WARNING: Subroutine does not return */
    FUN_700dca28();
  }
  FUN_7006e34c(uVar4,uVar3);
  return;
}


// ===== 0x700a959c -> FUN_700a959c @ 700a959c

undefined8
FUN_700a959c(undefined4 *param_1,undefined4 *param_2,undefined4 *param_3,undefined8 param_4,
            undefined4 *param_5,undefined4 *param_6,undefined4 *param_7)

{
  undefined4 uVar1;
  
  if ((param_1 != (undefined4 *)0x0) && (param_5 != (undefined4 *)0x0)) {
    uVar1 = FUN_700a953c();
    if (param_2 <= param_1 && param_1 < param_3) {
      *param_1 = uVar1;
      uVar1 = FUN_700a956c();
      if (param_6 <= param_5 && param_5 < param_7) {
        *param_5 = uVar1;
        return 0;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_700f03f0();
  }
                    /* WARNING: Subroutine does not return */
  FUN_70089c9c(0xacd0d4e3949a959,0x76);
}


