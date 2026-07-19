void* fn_27_1AF904(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 286) idx -= 286;
    return (char*)p + idx * 4 + 12;
}
