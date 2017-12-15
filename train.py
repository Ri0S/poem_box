import torch
import torch.nn as nn
import numpy as np
from torch.autograd import Variable
from data_utils import Corpus

embed_size = 256
hidden_size = 256
num_layers = 1
num_epochs = 4
num_samples = 5000  # number of words to be sampled
batch_size = 20
seq_length = 7
learning_rate = 0.0005

train_path = './data/random_half_less10_up5_newline_replaced.txt'
sample_path = './train_sample.txt'
corpus = Corpus()
ids = corpus.get_data(train_path, batch_size)
vocab_size = len(corpus.dictionary)
num_batches = ids.size(1) // seq_length


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


model = RNNLM(vocab_size, embed_size, hidden_size, num_layers)
model.cuda()
model.load_state_dict(torch.load('./model/kernel7_random_half_less10_up5_newline_replaced_12.pkl', map_location=lambda storage, loc: storage))

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


def detach(states):
    return [state.detach() for state in states]


for epoch in range(16, 16 + num_epochs):
    states = (Variable(torch.zeros(num_layers, batch_size, hidden_size)).cuda(),
              Variable(torch.zeros(num_layers, batch_size, hidden_size)).cuda())

    for i in range(0, ids.size(1) - seq_length, seq_length):
        inputs = Variable(ids[:, i:i + seq_length]).cuda()
        targets = Variable(ids[:, (i + 1):(i + 1) + seq_length].contiguous()).cuda()

        model.zero_grad()
        states = detach(states)
        outputs, states = model(inputs, states)
        loss = criterion(outputs, targets.view(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm(model.parameters(), 0.5)
        optimizer.step()

        step = (i + 1) // seq_length
        if step % 100 == 0:
            print('Epoch [%d/%d], Step[%d/%d], Loss: %.3f, Perplexity: %5.2f' %
                  (epoch, num_epochs, step, num_batches, loss.data[0], np.exp(loss.data[0])))

    torch.save(model.state_dict(), './model/kernel%d_random_half_less10_up5_newline_replaced_%d.pkl' % (seq_length, epoch))

with open(sample_path, 'wb') as f:
    state = (Variable(torch.zeros(num_layers, 1, hidden_size)).cuda(),
             Variable(torch.zeros(num_layers, 1, hidden_size)).cuda())

    prob = torch.ones(vocab_size)
    input = Variable(torch.multinomial(prob, num_samples=seq_length).unsqueeze(0),
                     volatile=True).cuda()

    for i in range(num_samples):
        output, state = model(input, state)

        prob = output[seq_length-1].squeeze().data.exp().cpu()
        word_id = torch.multinomial(prob, 1)[0]

        for idx in range(seq_length-1):
            input.data[0][idx] = input.data[0][idx+1]
        input.data[0][seq_length-1] = word_id


        word = corpus.dictionary.idx2word[word_id]
        word = '\n' if word == '<eos>' else word + ' '
        f.write(word.encode('utf-8'))

        if (i + 1) % 100 == 0:
            print('Sampled [%d/%d] words and save to %s' % (i + 1, num_samples, sample_path))
