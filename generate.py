import torch
import torch.nn as nn
from torch.autograd import Variable
from data_utils import Corpus

embed_size = 256
hidden_size = 256
batch_size = 20
num_layers = 1

seq_length = None
corpus_path = None
sample_path = None
corpus = None
vocab_size = None
num_batches = None
model = None

class RNNLM(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size, num_layers):
        super(RNNLM, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)
        self.init_weights()

    def init_weights(self):
        self.embed.weight.data.uniform_(-0.1, 0.1)
        self.linear.bias.data.fill_(0)
        self.linear.weight.data.uniform_(-0.1, 0.1)

    def forward(self, x, h):
        x = self.embed(x)
        out, h = self.lstm(x, h)
        out = out.contiguous().view(out.size(0) * out.size(1), out.size(2))
        out = self.linear(out)
        return out, h


def setup(seq_len, corpus_name, model_name):
    global seq_length, corpus_path, sample_path, corpus, vocab_size, model

    seq_length = seq_len

    corpus_path = './data/' + corpus_name
    sample_path = './sample/sample.txt'

    corpus = Corpus()
    corpus.get_data(corpus_path, batch_size)
    vocab_size = len(corpus.dictionary)

    model = RNNLM(vocab_size, embed_size, hidden_size, num_layers)
    model = model.cuda()
    model.load_state_dict(torch.load('./model/' + model_name, map_location=lambda storage, loc: storage))


def gen(seed):
    with open(sample_path , 'wb') as f:
        state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                 Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
        prob = torch.ones(vocab_size)

        try:
            input_seq = [corpus.dictionary.word2idx[seed]]
            state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                     Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
            for i in range(seq_length - 1):
                out, state = model(Variable(torch.LongTensor(input_seq).unsqueeze(0), volatile=True).cuda(), state)
                prob = out[i].squeeze().data.exp().cpu()
                word_id = torch.multinomial(prob, 1)[0]
                input_seq.append(word_id)
            input_seq[0] = corpus.dictionary.word2idx[seed]
            input_seq = Variable(torch.LongTensor(input_seq).unsqueeze(0), volatile=True).cuda()
        except KeyError:
            input_seq = Variable(torch.multinomial(prob, num_samples=seq_length).unsqueeze(0), volatile=True).cuda()

        while True:
            output, state = model(input_seq, state)
            prob = output[seq_length-1].squeeze().data.exp().cpu()
            word_id = torch.multinomial(prob, 1)[0]
            word = corpus.dictionary.idx2word[word_id]
            print(word, end=' ')
            if '+++$+++' in word:
                word = '\n'
            elif word == '<eos>':
                break
            else:
                word += ' '
            f.write(word.encode('utf-8'))

            for i in range(seq_length-1):
                input_seq.data[0][i] = input_seq.data[0][i+1]
            input_seq.data[0][seq_length-1] = word_id


def gen2(seed):
    with open(sample_path, 'wb') as f:
        state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                 Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
        prob = torch.ones(vocab_size)

        try:
            input_seq = [corpus.dictionary.word2idx[seed]]
            state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                     Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
            for i in range(seq_length - 1):
                out, state = model(Variable(torch.LongTensor(input_seq).unsqueeze(0), volatile=True).cuda(), state)
                prob = out[i].squeeze().data.exp().cpu()
                word_id = torch.multinomial(prob, 1)[0]
                input_seq.append(word_id)

            input_seq = Variable(torch.LongTensor(input_seq).unsqueeze(0), volatile=True).cuda()
        except KeyError:
            input_seq = Variable(torch.multinomial(prob, num_samples=seq_length).unsqueeze(0), volatile=True).cuda()

        flag = False

        while True:
            output, state = model(input_seq, state)
            prob = output[seq_length-1].squeeze().data.exp().cpu()
            word_id = torch.multinomial(prob, 1)[0]
            word = corpus.dictionary.idx2word[word_id]
            if not flag:
                if '+++$+++' in word:
                    flag = True
            else:
                if word == '<eos>':
                    break
                elif '+++$+++' in word:
                    word = '\n'
                elif word == '☆':
                    word = ' '
                f.write(word.encode('utf-8'))

                for i in range(seq_length-1):
                    input_seq.data[0][i] = input_seq.data[0][i+1]
                input_seq.data[0][seq_length-1] = word_id


if __name__ == '__main__':
    setup(5, 'random_half_less10_up5_newline_replaced.txt', 'kernel5_random_half_less10_up5_newline_replaced_0.pkl')
    gen('전쟁')
