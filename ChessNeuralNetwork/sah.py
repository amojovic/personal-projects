import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import chess.pgn
import random
import os
from torch.nn.utils.rnn import pad_sequence

class ChessDataset(Dataset):
    def __init__(self, pgn_file):
        self.games = []
        with open(pgn_file, 'r') as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                moves = list(game.mainline_moves())
                self.games.append(moves)

    def __len__(self):
        return len(self.games)

    def __getitem__(self, idx):
        moves = self.games[idx]
        input_moves = moves[:-1]  
        target_move = moves[-1]  

        input_tensors = torch.tensor([hash(move.uci()) % 10000 for move in input_moves], dtype=torch.long)
        target_tensor = torch.tensor(hash(target_move.uci()) % 10000, dtype=torch.long)

        return input_tensors, target_tensor



class ChessModel(nn.Module):
    def __init__(self, vocab_size=10000, embed_dim=128, hidden_dim=256, output_dim=10000):
        super(ChessModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.embedding(x)
        _, (hidden, _) = self.lstm(x)
        return self.fc(hidden[-1])



def train_model(model, data_loader, save_path, epochs=5, lr=0.001):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for inputs, target in data_loader:
            inputs = pad_sequence(inputs, batch_first=True)
            target = torch.stack(target)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, target)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(data_loader)}")

    
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")



def load_model(model, save_path):
    if os.path.exists(save_path):
        model.load_state_dict(torch.load(save_path, weights_only=True))
        print(f"Model loaded from {save_path}")
        return model
    else:
        print(f"No saved model found at {save_path}. Training a new model.")
        return model


def play_game(model):
    board = chess.Board()
    print(board)

    while not board.is_game_over():
        user_move = input("Your move: ")
        try:
            board.push_san(user_move)
        except ValueError:
            print("Invalid move. Try again.")
            continue

        print(board)
        print()  

        legal_moves = [move.uci() for move in board.legal_moves]

        if not legal_moves:
            print("No legal moves available. The game is over.")
            break

        input_tensor = torch.tensor([hash(move) % 10000 for move in legal_moves], dtype=torch.long)
        input_tensor = input_tensor.unsqueeze(0)

        with torch.no_grad():
            model.eval()
            output = model(input_tensor)
            best_move_idx = output.argmax().item()

            best_move_idx = best_move_idx % len(legal_moves)

        best_move = chess.Move.from_uci(legal_moves[best_move_idx])

        if best_move in board.legal_moves:
            board.push(best_move)
            print("AI's move:", legal_moves[best_move_idx])
        else:
            print("Model made an invalid move. Game over.")
            break

        print("AI's move:")
        print(board)
        print()  



if __name__ == "__main__":
    pgn_file = "games.pgn" 
    model_save_path = "chess_model.pth"
    batch_size = 32
    epochs = 5
    lr = 0.001

    dataset = ChessDataset(pgn_file)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=lambda x: list(zip(*x)))
    model = ChessModel()

    model = load_model(model, model_save_path)
    if not os.path.exists(model_save_path):
        train_model(model, data_loader, model_save_path, epochs, lr)

    play_game(model)
