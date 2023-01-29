import xopen
from Bio import SeqIO
import tqdm
#Create argparser
from io import TextIOWrapper
import argparse
import pyximport; pyximport.install()
from . import getdiffs
import concurrent.futures
import  threading, queue
from multiprocessing import Queue
import multiprocessing


names_so_far = set()

def read_file(input_file, skip, queue2):
    stream = xopen.xopen(input_file, 'rb')
    stream.seek(skip)
    text_stream = TextIOWrapper(stream, encoding='utf-8')
    records = SeqIO.parse(text_stream, 'fasta')
    batch = []
    batch_size = 100
    for record in tqdm.tqdm(records, total=7e6):
        batch.append(record)
        if len(batch) >= batch_size:
            queue2.put(batch)
            batch = []
    queue2.put(None)

def compare_strings_with_ref(ref_seq, record):
    other_seq = str(record.seq)
    other_seq = other_seq.upper()
    diffs = getdiffs.compare_strings(ref_seq, other_seq)
    return (record.id, diffs)



def queue_to_iterable(queue2):
    while True:
        item = queue2.get()
        if item is None:
            break
        yield item
def main(reference_file, target_file, skip):
    ref = SeqIO.read(reference_file, 'fasta')
    ref_seq = str(ref.seq)
    ref_seq = ref_seq.upper()

    queue2 = multiprocessing.Queue()

    p = multiprocessing.Process(target=read_file, args=(target_file,skip, queue2))
    p.start()
    



    for batch in queue_to_iterable(queue2):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        futures = [executor.submit(compare_strings_with_ref, ref_seq, record) for record in batch]
        for future in concurrent.futures.as_completed(futures):
            name, diffs = future.result()
            print(f"{name}\t{','.join([str(x) for x in diffs])}")
        



def console():
    parser = argparse.ArgumentParser(description='Alignment')
    parser.add_argument('input', help='Input aligned fasta')
    parser.add_argument('--reference',
                        help='Input reference sequence',
                        required=True)
    parser.add_argument('--skip',
                        help='Skip first n bytes of input',
                        type=int,
                        default=0)

    args = parser.parse_args()
    main(args.reference, args.input, args.skip)
    





if __name__ == "__main__":
    console()

