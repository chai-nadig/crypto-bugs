import matplotlib.pyplot as plt

from generate import is_combo, get_combo_key


def generate_bar_graph_from_counts(
        background_counts, spots_counts, color_counts, accessory_counts, eyes_counts, combo_counts
):
    all_counts = []

    all_counts.extend([(f'Background:{key}', value) for key, value in background_counts.items()])
    all_counts.extend([(f'Spots:{key}', value) for key, value in spots_counts.items()])
    all_counts.extend([(f'Color:{key}', value) for key, value in color_counts.items()])
    all_counts.extend([(f'Accessory:{key}', value) for key, value in accessory_counts.items()])
    all_counts.extend([(f'Eyes:{key}', value) for key, value in eyes_counts.items()])
    all_counts.extend([(f'Combo:{key}', value) for key, value in combo_counts.items()])

    all_counts = sorted(all_counts, key=lambda c: -c[1])

    plt.style.use('ggplot')

    traits = [c[0] for c in all_counts]
    counts = [c[1] for c in all_counts]
    colors = [get_color_for_trait(t[0]) for t in all_counts]

    plt.figure(figsize=(20, len(traits) / 4.0))
    container = plt.barh(traits, counts, color=colors)
    plt.bar_label(container, counts)
    plt.xlabel("Trait")
    plt.ylabel("Counts")
    plt.title("Trait counts across all traits")

    plt.savefig('trait_counts.png')

    print("total ticks", len(traits), len(counts))


def get_color_for_trait(t):
    if 'Background' in t:
        return 'green'

    if 'Spots' in t:
        return 'blue'

    if 'Color' in t:
        return 'red'

    if 'Accessory' in t:
        return 'black'

    if 'Eyes' in t:
        return 'Cyan'

    if 'Combo' in t:
        return 'orange'

    return 'pink'


def calculate_scores(background_counts, spots_counts, color_counts, accessory_counts, eyes_counts, combo_counts,
                     traits):
    background_scores = get_scores_for_counts(background_counts)
    spots_scores = get_scores_for_counts(spots_counts)
    color_scores = get_scores_for_counts(color_counts)
    accessory_scores = get_scores_for_counts(accessory_counts)
    eyes_scores = get_scores_for_counts(eyes_counts)
    combo_scores = get_scores_for_counts(combo_counts)

    trait_scores = []
    for trait in traits:
        b = background_scores[trait['Background']]
        s = spots_scores[trait['Spots']]
        c = color_scores[trait['Color']]
        a = accessory_scores[trait['Accessory']]
        e = eyes_scores[trait['Eyes']]
        cb = 0

        if is_combo(trait):
            cb = combo_scores[get_combo_key(trait)]

        trait_scores.append(b + s + c + a + e + cb)

    return trait_scores


def get_scores_for_counts(counts):
    max_count = max(counts.values())
    return {
        key: max_count / (count * 1.0) for key, count in counts.items()
    }


def generate_histogram_from_scores(scores):
    total = float(len(scores))

    scores = [s for s in scores if s <= 100]
    # scores = sorted(scores, key=lambda s: -s)

    num_bins = 50

    # the histogram of the data
    plt.figure(figsize=(num_bins / 2.0, 6))

    n, bins, patches = plt.hist(scores, bins=num_bins, facecolor='g', alpha=0.75, rwidth=0.5, )

    plt.xlabel('Scores')

    print('\n\nnumber of scores', len(scores))
    print('max scores', max(scores))

    plt.xlim(0, max(scores))
    plt.ylabel('Counts')
    plt.title('Histogram of Scores')
    plt.grid(True)
    plt.bar_label(patches, n)

    percentiles = [25.0, 50.0, 75.0, 90.0, 99.0]
    count = 0.0
    min_ylim, max_ylim = plt.ylim()
    for i in range(len(n)):
        v = n[i]
        count += v

        p_count = (percentiles[0] * total / 100) if len(percentiles) > 0 else None

        if p_count is not None and count >= p_count:
            mid = (bins[i] + bins[i + 1]) / 2

            plt.axvline(mid + 0.5, color='red', linestyle='dashed', linewidth=2)

            actual_percentile = count / total * 100

            plt.text(mid + 0.6, max_ylim * 0.9,
                     'P{:.2f}\n({})'.format(actual_percentile, count), color='red')

            while len(percentiles) > 0 and percentiles[0] <= actual_percentile:
                percentiles.pop(0)

    plt.savefig('scores.png')
