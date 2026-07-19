void* fn_27_1AF6D4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 448) idx -= 448;
    return (char*)p + idx * 4 + 12;
}
