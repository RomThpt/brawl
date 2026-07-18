extern int fn_100_CDB8();

int fn_100_BEEC(void* p) {
    return fn_100_CDB8((char*)p + (4));
}
