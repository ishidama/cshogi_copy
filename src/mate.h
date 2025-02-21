﻿#ifndef MATE_H
#define MATE_H

// 奇数手詰めチェック
// 詰ます手を返すバージョン
template <bool INCHECK>
Move mateMoveInOddPlyReturnMove(Position& pos, const int depth);

// 奇数手詰めチェック
template <bool INCHECK>
bool mateMoveInOddPly(Position& pos, const int depth);

// 偶数手詰めチェック
// 手番側が王手されていること
bool mateMoveInEvenPly(Position& pos, const int depth);

#endif
