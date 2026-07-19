void* fn_27_D96B0(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 24) + i;
    if (idx >= 106) idx -= 106;
    return (char*)p + idx * 48 + 12;
}
