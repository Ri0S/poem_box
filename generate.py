import torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from data_utils import Dictionary, Corpus

# Hyper Parameters
embed_size = 256
hidden_size = 256
num_layers = 1

seq_length = 5

corpus_path = './data/random_file_less10_up5_newline_replaced_drop_half.txt'
sample_path = './sample/sample.txt'

corpus = Corpus()
ids = corpus.get_data(corpus_path, batch_size)
vocab_size = len(corpus.dictionary)
num_batches = ids.size(1) // seq_length


# RNN Based Language Model
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
        # Embed word ids to vectors
        x = self.embed(x)

        # Forward propagate RNN
        out, h = self.lstm(x, h)

        # Reshape output to (batch_size*sequence_length, hidden_size)
        out = out.contiguous().view(out.size(0) * out.size(1), out.size(2))

        # Decode hidden states of all time step
        out = self.linear(out)
        return out, h


def generate(seed):
    with open(sample_path, 'wb') as f:
        state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                 Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
        prob = torch.ones(vocab_size)

        try:
            input = [corpus.dictionary.word2idx[seed]]
            state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                     Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
            for i in range(seq_length - 1):
                out, state = model(Variable(torch.LongTensor(input).unsqueeze(0), volatile=True).cuda(), state)
                prob = out[i].squeeze().data.exp().cpu()
                word_id = torch.multinomial(prob, 1)[0]
                input.append(word_id)

            input = Variable(torch.LongTensor(input).unsqueeze(0), volatile=True).cuda()
        except KeyError:
            input = Variable(torch.multinomial(prob, num_samples=seq_length).unsqueeze(0), volatile=True).cuda()

        while(True):
            output, state = model(input, state)
            prob = output[seq_length-1].squeeze().data.exp().cpu()
            word_id = torch.multinomial(prob, 1)[0]
            word = corpus.dictionary.idx2word[word_id]

            if '+++$+++' in word:
                word = '\n'
            elif word == '<eos>':
                break
            else:
                word += ' '
            f.write(word.encode('utf-8'))

            for i in range(seq_length-1):
                input.data[0][i] = input.data[0][i+1]
            input.data[0][seq_length-1] = word_id


model = RNNLM(vocab_size, embed_size, hidden_size, num_layers).cuda()
# model = RNNLM(488760, embed_size, hidden_size, num_layers)
model.load_state_dict(torch.load('model_kernel5_less10_up5_nlr_epoch0.pkl', map_location=lambda storage, loc: storage))
if __name__ == '__main__':
    for idx in range(3):
        model.load_state_dict(torch.load('model_kernel5_less10_up5_nlr_epoch%d.pkl' % idx, map_location=lambda storage, loc: storage))
        sample_path = './sample%d.txt' % idx
        with open(sample_path, 'wb') as f:
            # Set intial hidden ane memory states
            state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                     Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())

            # Select one word id randomly
            prob = torch.ones(vocab_size)

            seed = '사랑'
            try:
                input = [corpus.dictionary.word2idx[seed]]
                state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                         Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
                for i in range(seq_length-1):
                    out, state = model(Variable(torch.LongTensor(input).unsqueeze(0), volatile=True).cuda(), state)
                    prob = out[i].squeeze().data.exp().cpu()
                    word_id = torch.multinomial(prob, 1)[0]
                    input.append(word_id)

                input = Variable(torch.LongTensor(input).unsqueeze(0), volatile=True).cuda()
            except KeyError:
                input = Variable(torch.multinomial(prob, num_samples=5).unsqueeze(0), volatile=True).cuda()

            for i in range(2000):
                # Forward propagate rnn
                output, state = model(input, state)

                # Sample a word id
                prob = output[4].squeeze().data.exp().cpu()
                word_id = torch.multinomial(prob, 1)[0]

                # Feed sampled word id to next time step

                # input.data[0][0] = input.data[0][1]
                input.data[0][0] = corpus.dictionary.word2idx[seed]
                input.data[0][1] = input.data[0][2]
                input.data[0][2] = input.data[0][3]
                input.data[0][3] = input.data[0][4]
                input.data[0][4] = word_id

                # File write

                word = corpus.dictionary.idx2word[word_id]

                # word = '\n' if word == '<eos>' else word + ' '
                if '+++$+++' in word:
                    word = '\n'
                elif word == '<eos>':
                    word = '\n'
                    # break
                    word += '+++$+++\n'
                    try:
                        input = [corpus.dictionary.word2idx[seed]]
                        state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
                                 Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())
                        for i in range(seq_length - 1):
                            out, state = model(Variable(torch.LongTensor(input).unsqueeze(0), volatile=True).cuda(), state)
                            prob = out[i].squeeze().data.exp().cpu()
                            word_id = torch.multinomial(prob, 1)[0]
                            input.append(word_id)

                        input = Variable(torch.LongTensor(input).unsqueeze(0), volatile=True).cuda()
                    except KeyError:
                        input = Variable(torch.multinomial(prob, num_samples=5).unsqueeze(0), volatile=True).cuda()
                else:
                    word += ' '
                f.write(word.encode('utf-8'))


            print('Sample %d save to %s'% (idx, sample_path))
