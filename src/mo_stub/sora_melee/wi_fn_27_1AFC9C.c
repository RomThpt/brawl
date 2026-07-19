void* fn_27_1AFC9C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 309) idx -= 309;
    return (char*)p + idx * 4 + 12;
}
