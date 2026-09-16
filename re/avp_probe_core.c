// ===== 0x0011f80c -> FUN_0011f80c @ 0011f80c

void FUN_0011f80c(undefined8 *param_1)

{
  *param_1 = 0x7002ad88;
  param_1[1] = 0x7002ad88;
  FUN_00122f68();
  return;
}


// ===== 0x0012bf34 -> FUN_0012bf34 @ 0012bf34

void FUN_0012bf34(long param_1)

{
  ulong uVar1;
  long local_30;
  long local_28;
  
  if (param_1 != 0) {
    local_30 = 0;
    local_28 = 0;
    FUN_0012c87c(&local_30,&local_28);
    if (((local_30 == 0) || (uVar1 = FUN_0012c418(local_30,param_1), (uVar1 & 1) == 0)) &&
       ((local_28 == 0 || (uVar1 = FUN_0012c418(local_28,param_1), (uVar1 & 1) == 0)))) {
                    /* WARNING: Subroutine does not return */
      FUN_0012e8b0();
    }
  }
  return;
}


