# patch apfsprogs mkapfs to create TWO volumes: 0 = <-L label> role Preboot (0x10), 1 = "System" role System (0x1)
# iBoot fsboot mounts /boot by role Preboot and looks up role System for the sealed root hash (FUN_700a63a0).
# usage (WSL): python3 apfsprogs_multivol.py ~/kbuild/apfsprogs && make -C ~/kbuild/apfsprogs/mkapfs
import re, sys

root = sys.argv[1] + "/mkapfs/"


def edit(name, pairs):
    p = root + name
    s = open(p).read()
    for old, new in pairs:
        assert s.count(old) == 1, f"{name}: anchor not unique/missing: {old[:60]!r}"
        s = s.replace(old, new)
    open(p, "w").write(s)


edit("mkapfs.h", [
    ("#define FIRST_VOL_BNO\t\t\t(CPOINT_END + 2)",
     "#define NVOLS\t\t\t\t6\n"
     "#define VOL_BASE(i)\t\t\t(CPOINT_END + 2 + 8 * (i))\n"
     "#define VOL_OID(i)\t\t\t((i) ? APFS_OID_RESERVED_COUNT + 50 + ((i) - 1) * 2 : FIRST_VOL_OID)\n"
     "#define VOL_CAT_ROOT_OID(i)\t\t((i) ? APFS_OID_RESERVED_COUNT + 51 + ((i) - 1) * 2 : FIRST_VOL_CAT_ROOT_OID)\n"
     "#define FIRST_VOL_BNO\t\t\t(CPOINT_END + 2)"),
    # each vol uses 6 blocks at stride 8; 6 vols end at CPOINT_END+47, so IP bitmap starts at +50
    ("#define IP_BMAP_BASE\t\t\t(CPOINT_END + 10)", "#define IP_BMAP_BASE\t\t\t(CPOINT_END + 50)"),
])

edit("btree.h", [("extern void make_omap_btree(u64 bno, bool is_vol);",
                  "extern void make_omap_btree(u64 bno, bool is_vol, int vol);")])

edit("btree.c", [
    ("static void make_omap_root(u64 bno, bool is_vol)", "static void make_omap_root(u64 bno, bool is_vol, int vol)"),
    ("""	root->btn_nkeys = cpu_to_le32(1);
	toc_len = min_table_size(APFS_OBJECT_TYPE_OMAP);
	key_len = 1 * sizeof(*key);
	val_len = 1 * sizeof(*val);""",
     """	int n = is_vol ? 1 : NVOLS, i;

	root->btn_nkeys = cpu_to_le32(n);
	toc_len = min_table_size(APFS_OBJECT_TYPE_OMAP);
	key_len = n * sizeof(*key);
	val_len = n * sizeof(*val);"""),
    ("""	key = (void *)root + head_len + toc_len;
	val = (void *)root + param->blocksize - info_len - val_len;
	kvoff = (void *)root + head_len;
	kvoff->k = 0;
	kvoff->v = cpu_to_le16(val_len);

	/* Set the key and value for the one record */
	if (is_vol) {
		/* Map for the catalog root */
		key->ok_oid = cpu_to_le64(FIRST_VOL_CAT_ROOT_OID);
		val->ov_paddr = cpu_to_le64(FIRST_VOL_CAT_ROOT_BNO);
	} else {
		/* Map for the one volume superblock */
		key->ok_oid = cpu_to_le64(FIRST_VOL_OID);
		val->ov_paddr = cpu_to_le64(FIRST_VOL_BNO);
	}
	key->ok_xid = cpu_to_le64(MKFS_XID);
	val->ov_size = cpu_to_le32(param->blocksize); /* Only size supported */
""",
     """	for (i = 0; i < n; i++) {
		key = (void *)root + head_len + toc_len + i * sizeof(*key);
		val = (void *)root + param->blocksize - info_len - (i + 1) * sizeof(*val);
		kvoff = (void *)root + head_len + i * sizeof(*kvoff);
		kvoff->k = cpu_to_le16(i * sizeof(*key));
		kvoff->v = cpu_to_le16((i + 1) * sizeof(*val));
		if (is_vol) {
			/* Map for the catalog root */
			key->ok_oid = cpu_to_le64(VOL_CAT_ROOT_OID(vol));
			val->ov_paddr = cpu_to_le64(VOL_BASE(vol) + 3);
		} else {
			/* Map for volume superblock i (oids ascending) */
			key->ok_oid = cpu_to_le64(VOL_OID(i));
			val->ov_paddr = cpu_to_le64(VOL_BASE(i));
		}
		key->ok_xid = cpu_to_le64(MKFS_XID);
		val->ov_size = cpu_to_le32(param->blocksize); /* Only size supported */
	}
"""),
    ("set_omap_info((void *)root + param->blocksize - info_len, 1);",
     "set_omap_info((void *)root + param->blocksize - info_len, n);"),
    ("void make_omap_btree(u64 bno, bool is_vol)", "void make_omap_btree(u64 bno, bool is_vol, int vol)"),
    ("""		omap->om_tree_oid = cpu_to_le64(FIRST_VOL_OMAP_ROOT_BNO);
		make_omap_root(FIRST_VOL_OMAP_ROOT_BNO, is_vol);""",
     """		omap->om_tree_oid = cpu_to_le64(VOL_BASE(vol) + 2);
		make_omap_root(VOL_BASE(vol) + 2, is_vol, vol);"""),
    ("make_omap_root(MAIN_OMAP_ROOT_BNO, is_vol);", "make_omap_root(MAIN_OMAP_ROOT_BNO, is_vol, 0);"),
])

edit("super.c", [
    ("static void make_volume(u64 bno, u64 oid)\n{",
     "static void make_volume(int vol)\n{\n\tu64 bno = VOL_BASE(vol), oid = VOL_OID(vol);"),
    ("strcpy((char *)vsb->apfs_volname, param->label);",
     "{\n"
     "\tstatic const char *const vr_vol_names[6] = {0, \"System\", \"Data\", \"Update\", \"xART\", \"Hardware\"};\n"
     "\tstatic const u16 vr_vol_roles[6] = {0x10 /*Preboot*/, 0x1 /*System*/, 0x40 /*Data*/, 0xc0 /*Update*/, 0x100 /*xART*/, 0x140 /*Hardware*/};\n"
     "\tstrcpy((char *)vsb->apfs_volname, vol ? vr_vol_names[vol] : param->label);\n"
     "\tvsb->apfs_fs_index = cpu_to_le32(vol);\n"
     "\tvsb->apfs_role = cpu_to_le16(vr_vol_roles[vol]);\n"
     "\tvsb->apfs_vol_uuid[0] ^= (0x55 * vol);\n"
     "\t}"),
    ("""	vsb->apfs_omap_oid = cpu_to_le64(FIRST_VOL_OMAP_BNO);
	make_omap_btree(FIRST_VOL_OMAP_BNO, true /* is_vol */);
	vsb->apfs_root_tree_oid = cpu_to_le64(FIRST_VOL_CAT_ROOT_OID);
	make_cat_root(FIRST_VOL_CAT_ROOT_BNO, FIRST_VOL_CAT_ROOT_OID);""",
     """	vsb->apfs_omap_oid = cpu_to_le64(bno + 1);
	make_omap_btree(bno + 1, true /* is_vol */, vol);
	vsb->apfs_root_tree_oid = cpu_to_le64(VOL_CAT_ROOT_OID(vol));
	make_cat_root(bno + 3, VOL_CAT_ROOT_OID(vol));"""),
    ("""	vsb->apfs_extentref_tree_oid = cpu_to_le64(FIRST_VOL_EXTREF_ROOT_BNO);
	make_empty_btree_root(FIRST_VOL_EXTREF_ROOT_BNO,
			      FIRST_VOL_EXTREF_ROOT_BNO,""",
     """	vsb->apfs_extentref_tree_oid = cpu_to_le64(bno + 4);
	make_empty_btree_root(bno + 4,
			      bno + 4,"""),
    ("""	vsb->apfs_snap_meta_tree_oid = cpu_to_le64(FIRST_VOL_SNAP_ROOT_BNO);
	make_empty_btree_root(FIRST_VOL_SNAP_ROOT_BNO, FIRST_VOL_SNAP_ROOT_BNO,""",
     """	vsb->apfs_snap_meta_tree_oid = cpu_to_le64(bno + 5);
	make_empty_btree_root(bno + 5, bno + 5,"""),
    ("make_omap_btree(MAIN_OMAP_BNO, false /* is_vol */);", "make_omap_btree(MAIN_OMAP_BNO, false /* is_vol */, 0);"),
    ("""	sb_copy->nx_fs_oid[0] = cpu_to_le64(FIRST_VOL_OID);
	make_volume(FIRST_VOL_BNO, FIRST_VOL_OID);""",
     """	for (int v = 0; v < NVOLS; v++) {
		sb_copy->nx_fs_oid[v] = cpu_to_le64(VOL_OID(v));
		make_volume(v);
	}"""),
])

edit("spaceman.c", [
    ("		blocks += 6;			/* Volume superblock and its trees */",
     "		blocks += 6 * NVOLS;		/* Volume superblocks and their trees */"),
    ("	bmap_mark_as_used(bmap, FIRST_VOL_BNO, 6);",
     "	for (int v = 0; v < NVOLS; v++)\n\t\tbmap_mark_as_used(bmap, VOL_BASE(v), 6);"),
])
print("patched")
