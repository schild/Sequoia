# -*- encoding: UTF-8 -*-
import logging


# 低回撤稳步上涨策略
def check(code_name, data, end_date=None, threshold=60):
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    data = data.tail(n=threshold)

    if len(data) < threshold:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, threshold))
        return False

    ratio_increase = (data.iloc[-1]['close'] - data.iloc[0]['close']) / data.iloc[0]['close']
    if ratio_increase < 0.6:
        return False

    # 允许有一次“洗盘”
    flag = True
    return not any(
        data.iloc[i - 1]['p_change'] < -7
        or (data.iloc[i]['close'] - data.iloc[i]['open'])
        / data.iloc[i]['open']
        < -7 / 100
        or data.iloc[i - 1]['p_change'] + data.iloc[i]['p_change'] < -10
        or (data.iloc[i]['close'] - data.iloc[i - 1]['open'])
        / data.iloc[i - 1]['open']
        < -10 / 100
        for i in range(1, len(data))
    )
