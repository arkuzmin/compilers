
(A)   _t0 = 0;
(A)   i = _t0;
(A)   SUM = _t0;
// out {i, SUM}

// in {i, SUM}
  _L0:
(B)    _t1 = 20;
(B)    _t2 = i <= _t1;
(B)    ifZ _t2 Goto _L1;
// out {i, SUM} 

// in {i, SUM}
(C)   _t3 = 2; 
(C)    _t4 = _t3 * i;
(C)    _t5 = A + _t4;
(C)    _t6 = *(_t5);
(C)    _t7 = SUM + _t6;
(C)    SUM = _t7;
(C)    _t8 = 1;
(C)    _t9 = i + _t8;
(C)    i = _t9;
(C)    Goto _L0;
// out {i, SUM}
    
// in {i, SUM}
  _L1:
(D)    