// ===== 0x10d598 -> FUN_0010d580 @ 0010d580

void FUN_0010d580(long *param_1,long *param_2,long *param_3)

{
  long lVar1;
  
  if (param_1 < param_2 || param_3 <= param_1) {
                    /* WARNING: Subroutine does not return */
    FUN_0012ea7c();
  }
  while( true ) {
    lVar1 = *param_1;
    if ((int)*(uint *)(lVar1 + 0x14) < 0) break;
    *(uint *)(lVar1 + 0x10) = *(uint *)(lVar1 + 0x10) | 1;
    *(uint *)(*param_1 + 0x14) = *(uint *)(lVar1 + 0x14) | 0x80000000;
  }
  return;
}


