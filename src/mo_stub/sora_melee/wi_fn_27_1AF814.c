void* fn_27_1AF814(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 293) idx -= 293;
    return (char*)p + idx * 4 + 12;
}
