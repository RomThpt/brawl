void* fn_27_D9200(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 24) + i;
    if (idx >= 64) idx -= 64;
    return (char*)p + idx * 48 + 12;
}
