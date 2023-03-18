import math

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from numpy import fmin

loc = plticker.MultipleLocator(base=10000.0)  # this locator puts ticks at regular intervals

playable_length = 150000

attack_map = {0: 8, 1: 44, 2: 88, 3: 220, 4: 352, 5: 570, 6: 790, 7: 1102, 8: 1410, 9: 1796, 10: 2185, 11: 2676, 12: 3197, 13: 3745, 14: 4369, 15: 5043, 16: 5700, 17: 6240, 18: 7280, 19: 8190, 20: 8740, 21: 9360, 22: 10930, 23: 11920, 24: 13100, 25: 13100, 26: 14560 }
attack_buckets = {(27, 28): 16380, (29, 30): 18730, (31, 32): 21840, (33, 36): 26210, (37, 42): 32770, (43, 48): 43670, (49, 63): 65530, (64, 100): 131050 }
decay_map = {0: 1168, 1: 1378, 2: 86, 3: 216, 4: 345, 5: 558, 6: 773, 7: 1088, 8: 1380, 9: 1758, 10: 2140, 11: 2620, 12: 3131, 13: 3666, 14: 4277, 15: 4937, 16: 5581, 17: 6111, 18: 7129, 19: 8020, 20: 8555, 21: 9167, 22: 10695, 23: 11665, 24: 12833, 25: 12833, 26: 131048 }
decay_buckets = {(27, 28): 16039, (29, 30): 18282, (31, 32): 21388, (33, 36): 25666, (37, 42): 32079, (43, 48): 42770, (49, 63): 64160, (64, 100): 128315 }

attack_map2 = {0: 1/8, 1: 1/44, 2: 1/88, 3: 1/220, 4: 1/352, 5: 1/570, 6: 1/790, 7: 1/1102, 8: 1/1410, 9: 1/1796, 10: 1/2185, 11: 1/2676, 12: 1/3197, 13: 1/3745, 14: 1/4369, 15: 1/5043, 16: 1/5700, 17: 1/6240, 18: 1/7280, 19: 1/8190, 20: 1/8740, 21: 1/9360, 22: 1/10930, 23: 1/11920, 24: 1/13100, 25: 1/13100, 26: 1/14560 }
attack_buckets2 = {(27, 28): 1/16380, (29, 30): 1/18730, (31, 32): 1/21840, (33, 36): 1/26210, (37, 42): 1/32770, (43, 48): 1/43670, (49, 63): 1/65530, (64, 100): 1/131050 }
decay_map2 = {0: 1/1168, 1: 1/1378, 2: 1/86, 3: 1/216, 4: 1/345, 5: 1/558, 6: 1/773, 7: 1/1088, 8: 1/1380, 9: 1/1758, 10: 1/2140, 11: 1/2620, 12: 1/3131, 13: 1/3666, 14: 1/4277, 15: 1/4937, 16: 1/5581, 17: 1/6111, 18: 1/7129, 19: 1/8020, 20: 1/8555, 21: 1/9167, 22: 1/10695, 23: 1/11665, 24: 1/12833, 25: 1/12833, 26: 131048 }
decay_buckets2 = {(27, 28): 1/16039, (29, 30): 1/18282, (31, 32): 1/21388, (33, 36): 1/25666, (37, 42): 1/32079, (43, 48): 1/42770, (49, 63): 1/64160, (64, 100): 1/128315 }

def get_attack_or_decay_length(value, is_attack):
    if is_attack:
        if value <= 26:
            return attack_map[value]
        else:
            for bucket_range in attack_buckets:
                if bucket_range[0] <= value <= bucket_range[1]:
                    return attack_buckets[bucket_range]
    else:
        if value <= 26:
            return decay_map[value]
        else:
            for bucket_range in decay_buckets:
                if bucket_range[0] <= value <= bucket_range[1]:
                    return decay_buckets[bucket_range]

def get_attack_or_decay_increment(value, is_attack):
    if is_attack:
        if value <= 26:
            return attack_map2[value]
        else:
            for bucket_range in attack_buckets2:
                if bucket_range[0] <= value <= bucket_range[1]:
                    return attack_buckets2[bucket_range]
    else:
        if value <= 26:
            return -decay_map2[value]
        else:
            for bucket_range in decay_buckets2:
                if bucket_range[0] <= value <= bucket_range[1]:
                    return -decay_buckets2[bucket_range]

def getEnvelopeAmplitude(attackTime, decayTime, attackIncrement, decayIncrement):
    global envelopeAmplitude

    def get_increment(myAttackTime, myDecayTime):
        if indexWithinPlayableLength < myAttackTime:
            return attackIncrement
        elif indexWithinPlayableLength < (playable_length - myDecayTime):
            return 0
        else:
            return decayIncrement

    if playable_length >= (attackTime + decayTime) * 1.005:
        envelopeAmplitude += get_increment(attackTime, decayTime)
        if attack_value == 0 and envelopeAmplitude > 0.83:
            envelopeAmplitude = 0.83
    else:
        hold_length = playable_length - (attackTime + decayTime)

        if hold_length < 0:
            hold_length = 0;

        remainder = playable_length - (attackTime + hold_length)

        if remainder < 0:
            remainder = 0

        relative_remainder = remainder / decayTime

        decayLeftShift = (1.0 - relative_remainder) * decayTime * 1.1

        attackTime -= decayLeftShift

        if indexWithinPlayableLength < attackTime:
            envelopeAmplitude += attackIncrement
        elif indexWithinPlayableLength >= attackTime + hold_length:
            if (playable_length - indexWithinPlayableLength) < 8:
                envelopeAmplitude -= 0.125
            else:
                envelopeAmplitude += - (((1.1 - (relative_remainder * 0.65)) ** 14) * 0.00003) - 0.000007

attack_value = 100
decay_value  = 100
tweak_attack_value = False
tweak_decay_value = True
plot_count = 7
fig, axs = plt.subplots(plot_count)

plot_counter = 0
plot_offset = 0

for value in range(0, 100, 10):
    if plot_offset > 0:
        plot_offset -= 1
        continue

    if value == 60:
        continue

    if tweak_attack_value:
        attack_value = value

    if tweak_decay_value:
        decay_value = value

    attack_length = get_attack_or_decay_length(attack_value, True)
    decay_length =  get_attack_or_decay_length(decay_value, False)
    attack_increment = get_attack_or_decay_increment(attack_value, True)
    decay_increment =  get_attack_or_decay_increment(decay_value, False)
    x = []
    y = []
    global indexWithinPlayableLength
    indexWithinPlayableLength = 0
    envelopeAmplitude = 0.0

    for i in range(playable_length):
        indexWithinPlayableLength = i
        x.append(i)
        y.append(envelopeAmplitude)
        getEnvelopeAmplitude(
            attack_length, decay_length, attack_increment, decay_increment
        )
    axs[plot_counter].plot(x,y)
    axs[plot_counter].xaxis.set_major_locator(loc)
    axs[plot_counter].set_ylim([0, 1.1])
    axs[plot_counter]

    plot_counter += 1
    if plot_counter >= plot_count:
        break

plt.xlabel('Frame')
plt.ylabel('Amplitude')

mng = plt.get_current_fig_manager()
mng.resize(1400, 1500)

plt.show()

decay_map = {0: 1062, 1: 1378, 2: 77, 3: 193, 4: 308, 5: 499, 6: 691, 7: 964, 8: 1234, 9: 1571, 10: 1912, 11: 2341, 12: 2798, 13: 3277, 14: 3823, 15: 4412, 16: 4988, 17: 5462, 18: 6371, 19: 7168, 20: 7646, 21: 8193, 22: 9558, 23: 10425, 24: 11469, 25: 11469, 26: 12742 }
decay_buckets = {(27, 28): 14334 }