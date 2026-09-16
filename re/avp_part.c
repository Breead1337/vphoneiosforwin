// ===== 0x00110b2c -> FUN_00110b2c @ 00110b2c

int FUN_00110b2c(char *param_1,char *param_2,char *param_3,undefined8 param_4,char *param_5,
                char *param_6,char *param_7,undefined8 param_8,long param_9)

{
  char *pcVar1;
  char *pcVar2;
  char cVar3;
  
  pcVar1 = param_1;
  pcVar2 = param_5;
  for (; param_9 != 0; param_9 = param_9 + -1) {
    if ((param_1 < param_2 || param_3 <= pcVar1) || (param_5 < param_6 || param_7 <= pcVar2)) {
                    /* WARNING: Subroutine does not return */
      FUN_0012ea7c();
    }
    cVar3 = *pcVar1 - *pcVar2;
    if (cVar3 != '\0') goto LAB_00110b88;
    if (*pcVar1 == '\0') break;
    pcVar1 = pcVar1 + 1;
    pcVar2 = pcVar2 + 1;
  }
  cVar3 = '\0';
LAB_00110b88:
  return (int)cVar3;
}


// ===== 0x00126a58 -> FUN_00126a58 @ 00126a58

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00126a58(void)

{
  long lVar1;
  
  lVar1 = _DAT_7002add8;
  FUN_00126494();
  if (_DAT_7002add8 == lVar1) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_00123c18();
}


