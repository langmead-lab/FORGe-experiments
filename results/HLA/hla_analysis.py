import csv
import codecs

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.plotly as py
import plotly.graph_objs as go

class CSVResults():
    def __init__(self, sample_id, content):
        self.sample_id = sample_id
        self.content = content
    
def read_csv(filename):
    sample_id = []
    content = []
    index = -1
    with codecs.open(filename, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if index > -1:
                sample_id.append(row[0])
                content.append(row[1:])
            index += 1
    typing_results = CSVResults(sample_id, content)
    return typing_results

def calc_coverage(coverage_info):
    avg_coverage = []
    for number in coverage_info.content:
        avg_coverage.append(float(number[0])*101/4/(33448354-28477797))
    return avg_coverage

def analyze_results(verified_data, typing_results, coverage_info, out_filename):
    num_called = []
    num_correct = []
    # recall = []
    # precision = []
    if typing_results.sample_id != coverage_info.sample_id:
        print 'ERROR: samples are not matched.'
        return
    for index, result in enumerate(typing_results.content):
        locus_matched = []
        locus_called = 0
        for locus in result:
            if locus.count('*') > 0:
                locus_called += 1
        # Use only one verified_data
        for v_locus in verified_data.content[0]:
            for index, locus in enumerate(result):
                if index not in locus_matched and locus.startswith(v_locus) and locus.count('*') is 1:
                    locus_matched.append(index)
                    break
        # recall.append(float(len(locus_matched))/12*100)
        # precision.append(float(len(locus_matched))/locus_called*100)
        num_correct.append(len(locus_matched))
        num_called.append(locus_called)
        # num_called.append(float(locus_called)/12*100)

    avg_coverage = calc_coverage(coverage_info)
    # Transpose results for CSV output
    results = [typing_results.sample_id, num_called, num_correct, avg_coverage]
    # results = [typing_results.sample_id, recall, precision, avg_coverage]
    results = zip(*results)

    # Write to CSV
    with open(out_filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['SNV', 'NumCalled', 'NumAcc', 'Coverage'])
        # writer.writerow(['SNV', 'Recall', 'Precision', 'Coverage'])
        for line in results:
            writer.writerow(line)

    return

verified_data = read_csv("verified_data.csv")
typing_results = read_csv("ERR194147-hs2-hs37d5-extract-kourami.csv")
coverage_info = read_csv("ERR194147-hs2-hs37d5-extract-fq.csv")
analyze_results(verified_data, typing_results, coverage_info, "HLA_results.csv")
