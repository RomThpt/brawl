void* fn_79_59EC(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 30) idx -= 30;
    return (char*)p + idx * 104 + 12;
}
