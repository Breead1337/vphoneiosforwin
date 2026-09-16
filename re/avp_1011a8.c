// ===== 0x1011a8 -> FUN_001011a8 @ 001011a8

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_001011a8(uint *param_1,uint *param_2,uint *param_3,undefined8 param_4,int *param_5,
                 int *param_6,int *param_7,undefined8 param_8,uint param_9,int *param_10,
                 int *param_11,int *param_12,undefined8 param_13,ulong param_14,undefined8 param_15,
                 undefined8 param_16,undefined8 param_17,ulong param_18,ulong *param_19,
                 ulong *param_20,ulong *param_21,undefined8 param_22,long param_23)

{
  byte bVar1;
  ulong uVar2;
  undefined1 uVar3;
  int iVar4;
  int iVar6;
  uint uVar7;
  uint uVar8;
  int iVar5;
  undefined8 uVar9;
  ulong uVar11;
  long lVar12;
  byte *pbVar13;
  undefined1 *puVar14;
  undefined **ppuVar15;
  int extraout_w8;
  int extraout_w8_00;
  int extraout_w8_01;
  int extraout_w8_02;
  int extraout_w8_03;
  undefined8 extraout_x8;
  ulong uVar16;
  ulong uVar17;
  ulong uVar18;
  undefined1 auVar19 [16];
  undefined1 auVar20 [16];
  int *local_498;
  byte local_441;
  undefined1 *local_440;
  undefined1 *puStack_438;
  undefined8 *local_430;
  undefined **ppuStack_428;
  ulong *local_420;
  ulong *puStack_418;
  undefined1 *local_410;
  undefined **local_408;
  int *piStack_400;
  int *local_3f8;
  ulong *local_3f0;
  undefined **local_3e8;
  undefined1 auStack_3e0 [16];
  byte *pbStack_3d0;
  undefined **local_3c8;
  undefined1 auStack_3c0 [4];
  int local_3bc;
  ulong local_3b8;
  ulong local_3b0;
  ulong local_3a8;
  undefined8 local_3a0;
  undefined8 uStack_398;
  undefined8 local_390;
  undefined8 uStack_388;
  undefined8 local_380;
  undefined8 uStack_378;
  byte abStack_370 [4];
  int local_36c;
  uint local_368;
  undefined1 local_364;
  undefined4 local_35c;
  undefined4 local_358;
  undefined1 auStack_354 [48];
  undefined1 auStack_324 [48];
  undefined4 local_2f4;
  undefined2 local_2f0;
  char local_2ee;
  byte local_2ed;
  byte local_2ec;
  byte local_2eb [2];
  byte local_2e9;
  char local_2e8;
  byte local_2e7;
  char local_2e4;
  ulong local_2e0;
  undefined8 local_2d8;
  ulong local_2d0;
  ulong local_2c8;
  undefined8 local_2c0;
  undefined1 auStack_2b8 [48];
  char local_288;
  byte local_287;
  byte local_286;
  byte local_285;
  undefined1 local_284;
  undefined1 local_283;
  undefined8 local_280;
  undefined2 local_278;
  undefined2 local_276;
  undefined2 local_274;
  undefined1 local_272;
  undefined1 auStack_271 [48];
  byte local_241;
  undefined1 local_240;
  byte local_23f;
  undefined1 auStack_238 [456];
  undefined8 local_70 [2];
  undefined1 *puVar10;
  
  FUN_00102af4();
  local_3a8 = 0;
  local_70[0] = extraout_x8;
  FUN_00110ed0(auStack_238,0x1c8);
  local_3b8 = 0;
  local_3b0 = 0;
  local_3bc = 0;
  FUN_00110ed0(&local_440,0x80);
  FUN_00110ed0(&local_2e0,0xa8);
  FUN_00110ed0(&local_36c,0x8c);
  local_380 = 0;
  uStack_378 = 0;
  local_390 = 0;
  uStack_388 = 0;
  local_3a0 = 0;
  uStack_398 = 0;
  DAT_7002ae30 = '\0';
  if ((param_1 == (uint *)0x0) || (param_14 == 0)) goto LAB_00101a8c;
  if (param_1 < param_2 || param_3 <= param_1) goto LAB_00101a90;
  if (param_18 < *param_1) {
    FUN_00102bd0();
    iVar4 = extraout_w8 + -0x25;
    goto LAB_00101280;
  }
  FUN_001113a0(&local_36c,&local_36c,&local_2e0,&PTR_LOOP_0013d618,0,0x8c);
  FUN_001113a0(&local_2e0,&local_2e0,auStack_238,&PTR_LOOP_0013d630,0,0xa8);
  local_2d0 = thunk_FUN_00105244();
  local_2d0 = local_2d0 & 0xffffffff;
  local_2e0 = thunk_FUN_0010524c();
  local_2e0 = local_2e0 & 0xffffffff;
  local_2c8 = thunk_FUN_0010523c();
  local_2c8 = local_2c8 & 0xffffffff;
  local_2d8 = thunk_FUN_0010525c();
  local_280 = thunk_FUN_00105224();
  local_278 = thunk_FUN_001051dc();
  local_276 = FUN_00124268();
  local_284 = FUN_00105da4();
  local_286 = 0;
  bVar1 = (byte)param_1[3];
  local_287 = bVar1 >> 2 & 1;
  local_285 = bVar1 >> 3 & 1;
  if ((bVar1 >> 3 & 1) == 0) {
    local_286 = FUN_00104a04();
  }
  iVar4 = FUN_0010475c(auStack_2b8,auStack_2b8,&local_288,0x70028430);
  local_288 = iVar4 == 0;
  local_283 = FUN_00123d90();
  local_274 = thunk_FUN_00123d28();
  if ((local_285 == 1) && ((local_287 & 1) == 0)) {
    local_2c0 = FUN_001046c4(0);
  }
  local_272 = FUN_00104860();
  ppuVar15 = &PTR_LOOP_0013ce48;
  pbVar13 = abStack_370;
  iVar4 = FUN_00104868(&local_3a0,&local_3a0,pbVar13,&PTR_LOOP_0013ce48,0x30);
  if (iVar4 == 0) {
    ppuVar15 = (undefined **)0x70028448;
    pbVar13 = &local_241;
    FUN_00111154(auStack_271,auStack_271,pbVar13,0x70028448,&local_3a0,&local_3a0,abStack_370,
                 &PTR_LOOP_0013ce48,0x30);
  }
  local_240 = thunk_FUN_00104858();
  auVar19 = FUN_00101bc0();
  uVar18 = (ulong)*param_1;
  iVar4 = FUN_00101bfc(param_1,param_2,param_3,param_14,param_15,param_16,param_17,uVar18);
  if (iVar4 == 0) {
    if ((*(byte *)((long)param_1 + 0xd) & 1) != 0) {
      if (param_19 != (ulong *)0x0) {
        if (param_19 < param_20 || param_21 <= param_19) goto LAB_00101a90;
        *param_19 = uVar18;
      }
LAB_00101508:
      uVar3 = DAT_7002ae30 == '\x01';
      if ((bool)uVar3) {
        if (_DAT_7002ae78 == (code *)0x0) goto LAB_00101938;
        (*_DAT_7002ae78)(1);
      }
      uVar9 = 0;
      goto LAB_00101490;
    }
    FUN_00102b24(&local_3a8);
    FUN_00102b14();
    iVar4 = FUN_00102b68();
    if (iVar4 == 0) {
      if (uVar18 < local_3a8) {
        FUN_00102bd0();
        iVar4 = extraout_w8_01 + -0x22;
      }
      else {
        FUN_001113a0(param_14 + local_3a8,param_15,param_16,param_17,0,uVar18 - local_3a8);
        uVar9 = thunk_FUN_00102b40(param_14,param_15,param_16,param_17);
        iVar4 = FUN_00129318(uVar9,local_3a8,auStack_238);
        if (iVar4 == 0) {
          iVar4 = FUN_00128b5c(auStack_238,&local_3bc);
          if (iVar4 != 0) goto LAB_00101458;
          if (_DAT_7002ae38 != (code *)0x0) {
            iVar4 = (*_DAT_7002ae38)(local_3bc);
            if (iVar4 != 0) {
              if (_DAT_7002ae78 == (code *)0x0) goto LAB_00101a8c;
              (*_DAT_7002ae78)(0);
              DAT_7002ae30 = '\x01';
            }
          }
          uVar18 = (ulong)param_9;
          local_498 = param_5;
          if (param_9 != 0) {
            do {
              if (uVar18 == 0) {
                FUN_00102bd0();
                iVar4 = extraout_w8_03 + -0x20;
                goto LAB_00101280;
              }
              if (local_498 < param_6 || param_7 <= local_498) goto LAB_00101a90;
              iVar4 = *local_498;
              uVar18 = uVar18 - 1;
              local_498 = local_498 + 1;
            } while (iVar4 != local_3bc);
          }
          iVar4 = 0x40040026;
          iVar5 = FUN_00128e6c(auStack_238,&local_2ed);
          iVar6 = local_3bc;
          auVar20._8_8_ = auStack_3e0._8_8_;
          auVar20._0_8_ = auStack_3e0._0_8_;
          uVar9 = 0x40040007;
          if ((iVar5 != 0) || (auStack_3e0 = auVar20, (local_2ed & 1) == 0)) goto LAB_001016f4;
          local_440 = auStack_238;
          local_430 = local_70;
          ppuStack_428 = &PTR_LOOP_0013d348;
          local_420 = &local_2e0;
          piStack_400 = &local_36c;
          local_408 = &PTR_LOOP_0013d630;
          local_3e8 = &PTR_LOOP_0013d618;
          puVar14 = auStack_3c0;
          puStack_438 = local_440;
          puStack_418 = local_420;
          local_410 = auStack_238;
          local_3f8 = piStack_400;
          local_3f0 = &local_2e0;
          pbStack_3d0 = pbVar13;
          local_3c8 = ppuVar15;
          auStack_3e0 = auVar19;
          auVar20 = FUN_00102ac4(&local_440,&local_440,puVar14,&PTR_LOOP_0013d648);
          puVar10 = auVar20._0_8_;
          if (puVar10 < auVar20._8_8_ || puVar14 <= puVar10) goto LAB_00101a90;
          if (*(long *)(puVar10 + 0x20) == 0) goto LAB_00101a8c;
          iVar6 = FUN_00129448(iVar6,auStack_238,&PTR_FUN_0013d810,auVar19._0_8_,&local_440);
          if (iVar6 != 0) {
            uVar9 = 0x40040008;
            goto LAB_001016f4;
          }
          iVar6 = FUN_0013c58c(auStack_238,auStack_354,0x30);
          if (iVar6 != 0) goto LAB_00101a8c;
          if (((((local_241 & 1) == 0) && ((local_23f & 1) == 0)) && ((local_286 & 1) != 0)) &&
             ((local_2f4 & 0x10000) == 0)) {
            uVar9 = 0x40040009;
            if (local_288 == '\x01') {
              iVar6 = FUN_001114fc(auStack_2b8,auStack_2b8,&local_288,0x70028430,auStack_354,
                                   auStack_354,auStack_324,0x70028460,0x30);
              if (iVar6 == 0) {
                local_2ec = 1;
                goto LAB_001017c0;
              }
            }
          }
          else {
LAB_001017c0:
            if ((char)local_2f0 == '\x01') {
              uVar7 = FUN_00105db4((undefined1)local_2f4);
              if ((uVar7 & 1) == 0) {
                uVar9 = 0x4004003e;
              }
              else {
                if (local_2f4 >> 0x18 == (uVar7 & 0xff00) >> 8) goto LAB_001017e8;
                uVar9 = 0x4004000a;
              }
            }
            else {
LAB_001017e8:
              if (local_2ee != '\x01') {
LAB_0010180c:
                if ((local_274 & 1) != 0) {
                  if ((local_2e7 & 1) == 0) {
                    if ((local_274 & 0x100) == 0) goto LAB_00101850;
                  }
                  else if (local_274._1_1_ == local_2e8) {
LAB_00101850:
                    local_441 = 0;
                    if (param_23 != 0) {
                      iVar6 = FUN_00128fa4(auStack_238,&local_441);
                      if ((iVar6 == 0) && ((local_441 & 1) != 0)) {
                        iVar6 = FUN_00101d90(auStack_238);
                        if (iVar6 != 0) {
                          iVar4 = 0x40040057;
                          goto LAB_00101280;
                        }
                      }
                    }
                    iVar6 = FUN_00128b18(auStack_238,&local_3b8);
                    uVar18 = local_3b0;
                    uVar2 = local_3b8;
                    if (iVar6 == 0) {
                      if (param_18 < local_3b0) {
                        iVar4 = 0x40040024;
                      }
                      else {
                        iVar6 = FUN_00128bc0(auStack_238,local_2eb);
                        if (iVar6 == 0) {
                          if (local_2eb[0] != 1) {
LAB_0010196c:
                            FUN_00102b88();
                            FUN_00102b14();
                            FUN_00111154();
joined_r0x00101988:
                            if (param_19 != (ulong *)0x0) {
                              if (param_19 < param_20 || param_21 <= param_19) goto LAB_00101a90;
                              *param_19 = uVar18;
                            }
                            if (uVar2 <= param_14) {
LAB_00101a8c:
                    /* WARNING: Subroutine does not return */
                              FUN_0010550c();
                            }
                            if (uVar18 < local_3a8) {
                              FUN_00102b14();
                              lVar12 = thunk_FUN_00102b40();
                              FUN_001113a0(lVar12 + uVar18);
                            }
                            if ((local_2f4._1_1_ != '\x01') || ((local_2e9 & 1) != 0)) {
                              FUN_00105eb4();
                              if ((local_2f4 & 0x100) == 0) {
                                FUN_00105d20();
                              }
                            }
                            FUN_00105d88((undefined1)local_2f4);
                            FUN_00105e68(local_3bc);
                            FUN_00105df8(auStack_354,auStack_354,auStack_324,0x70028460);
                            if (((local_2f4 & 0x10000) != 0) ||
                               ((uVar9 = 1, (local_285 & 1) == 0 && ((local_2ec & 1) == 0)))) {
                              uVar9 = 0;
                            }
                            FUN_00105e74(uVar9);
                            if (local_2e4 == '\x01') {
                              FUN_00105ec8();
                            }
                            if ((local_287 & 1) == 0) {
                              FUN_00105ea0();
                            }
                            if (param_10 != (int *)0x0) {
                              if (param_10 < param_11 || param_12 <= param_10) {
LAB_00101a90:
                    /* WARNING: Subroutine does not return */
                                FUN_0012ea7c();
                              }
                              *param_10 = local_3bc;
                            }
                            goto LAB_00101508;
                          }
                          iVar6 = FUN_00128bec(auStack_238,&local_36c);
                          uVar7 = local_368;
                          if (iVar6 == 0) {
                            if ((local_2eb[0] & 1) == 0) goto LAB_0010196c;
                            uVar17 = (ulong)local_368;
                            if (local_36c == 0) {
                              uVar16 = 0x2000;
                              uVar11 = 0;
                            }
                            else {
                              if (local_36c != 1) {
                                iVar4 = 0x40040025;
                                goto LAB_00101280;
                              }
                              uVar11 = FUN_00135e88(0x891);
                              uVar16 = 0xa400;
                            }
                            if (((!CARRY8(uVar11,uVar18)) && (!CARRY8(uVar11 + uVar18,uVar16))) &&
                               ((uVar11 + uVar18 + uVar16 <= param_18 &&
                                (((!CARRY8(uVar11,uVar17) && (!CARRY8(uVar11 + uVar17,uVar16))) &&
                                 (uVar11 + uVar17 + uVar16 <= param_18)))))) {
                              FUN_00102b14();
                              lVar12 = thunk_FUN_00102b40();
                              lVar12 = (lVar12 + param_18) - uVar11;
                              auVar19 = FUN_00102b88(lVar12 - uVar18);
                              uVar11 = auVar19._0_8_;
                              FUN_00111434();
                              if (local_36c == 0) {
                                uVar8 = FUN_00111858(param_14,uVar17,uVar11,uVar18);
                                if (uVar7 == uVar8) goto LAB_00101b5c;
                                iVar4 = 0x40040027;
                              }
                              else {
                                uVar18 = FUN_00135f20(param_14,uVar17,uVar11,uVar18,lVar12,0x891);
                                if (uVar18 == uVar17) {
LAB_00101b5c:
                                  FUN_00102b14();
                                  lVar12 = thunk_FUN_00102b40();
                                  if (uVar11 <= lVar12 + uVar17) {
                                    FUN_00102b14();
                                    auVar19 = thunk_FUN_00102b40();
                                    auVar19._8_8_ = auVar19._8_8_;
                                    auVar19._0_8_ = auVar19._0_8_ + uVar17;
                                  }
                                  FUN_001113a0(auVar19._0_8_,auVar19._8_8_);
                                  FUN_001275ac(0x40029);
                                  uVar18 = (ulong)local_368;
                                  goto joined_r0x00101988;
                                }
                                iVar4 = 0x40040028;
                              }
                            }
                          }
                          else {
                            iVar4 = 0x40040010;
                          }
                        }
                        else {
                          iVar4 = 0x4004000f;
                        }
                      }
                    }
                    else {
                      iVar4 = 0x4004000c;
                    }
                    goto LAB_00101280;
                  }
                }
                iVar4 = 0x40040046;
                goto LAB_00101280;
              }
              uVar7 = FUN_00124268();
              if ((uVar7 & 1) == 0) {
                uVar9 = 0x4004003f;
              }
              else {
                if ((uint)local_2f0._1_1_ == (uVar7 & 0xff00) >> 8) goto LAB_0010180c;
                uVar9 = 0x4004000b;
              }
            }
          }
LAB_001016f4:
          FUN_001275ac(uVar9);
          local_35c = 0;
          local_358 = 0;
          local_2f4 = 0;
          local_364 = 0;
          local_2f0 = 0;
          local_2ee = '\0';
          iVar4 = 0x40040023;
          local_2e4 = '\0';
        }
        else {
          FUN_00102bd0();
          iVar4 = extraout_w8_02 + -0x21;
        }
      }
    }
    else {
      FUN_00102bd0();
      iVar4 = extraout_w8_00 + -0x23;
    }
LAB_00101280:
    FUN_001275ac(iVar4);
  }
LAB_00101458:
  FUN_00102b14();
  FUN_001113a0();
  uVar3 = DAT_7002ae30 == '\x01';
  if ((bool)uVar3) {
    if (_DAT_7002ae78 == (code *)0x0) {
LAB_00101938:
                    /* WARNING: Subroutine does not return */
      FUN_0012e944();
    }
    (*_DAT_7002ae78)(0);
  }
  uVar9 = 0xffffffff;
LAB_00101490:
  FUN_00102ad0(local_70[0],uVar9);
  if ((bool)uVar3) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


