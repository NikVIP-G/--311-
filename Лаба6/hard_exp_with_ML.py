import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
from functools import lru_cache

"""
Используемые библиотеки:
- torch: основная библиотека PyTorch для тензорных операций
- torch.nn: для создания нейронных сетей
- torch.optim: для оптимизаторов
- torchvision: для работы с datasets и transforms
"""


def run():
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    train_dataset = torchvision.datasets.FashionMNIST(
        root='./data',
        train=True,
        download=True,
        transform=transform
    )

    test_dataset = torchvision.datasets.FashionMNIST(
        root='./data',
        train=False,
        download=True,
        transform=transform
    )

    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=32,
        shuffle=True
    )

    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=32,
        shuffle=False
    )

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    print("Типы вещей, которые распознает сеть:")
    for i, name in enumerate(class_names):
        print(f"{i}: {name}")

    # Покажем несколько примеров из каждого класса
    plt.figure(figsize=(15, 10))

    # Создаем словарь для хранения первых примеров каждого класса
    class_examples = {}

    # Однократно проходим по датасету и находим по одному примеру каждого класса
    for i in range(len(train_dataset)):
        image, label = train_dataset[i]
        if label not in class_examples:
            class_examples[label] = (image, label)
        if len(class_examples) == 10:  # Все 10 классов найдены
            break

    # Отображаем найденные примеры
    for i in range(10):
        image, label = class_examples[i]

        plt.subplot(2, 5, i + 1)
        plt.imshow(image.squeeze(), cmap='gray')
        plt.title(f'{class_names[label]}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Определение модели нейронной сети
    class FashionMNISTModel(nn.Module):
        def __init__(self):
            super(FashionMNISTModel, self).__init__()
            self.flatten = nn.Flatten()
            self.linear_relu_stack = nn.Sequential(
                nn.Linear(28 * 28, 128),
                nn.ReLU(),
                nn.Linear(128, 10)
            )

        def forward(self, x):
            x = self.flatten(x)
            logits = self.linear_relu_stack(x)
            return logits


    # Создание модели, функции потерь и оптимизатора
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FashionMNISTModel().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Обучение модели
    print("\nОбучение модели...")
    epochs = 10
    train_losses = []
    train_accuracies = []

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward pass и оптимизация
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Расчет точности
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(train_loader)
        epoch_accuracy = 100 * correct / total

        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_accuracy)

        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.2f}%')

    # Тестирование модели
    model.eval()
    test_correct = 0
    test_total = 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            test_total += labels.size(0)
            test_correct += (predicted == labels).sum().item()

    test_accuracy = 100 * test_correct / test_total
    print(f'\nТочность на тестовых данных: {test_accuracy:.2f}%')

    # Визуализация предсказаний
    def imshow(img):
        img = img / 2 + 0.5  # денормализация
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1, 2, 0)))
        plt.axis('off')


    # Покажем несколько тестовых примеров с предсказаниями
    model.eval()
    dataiter = iter(test_loader)
    images, labels = next(dataiter)
    images, labels = images.to(device), labels.to(device)

    with torch.no_grad():
        outputs = model(images)
        _, predictions = torch.max(outputs, 1)

    # Переводим обратно на CPU для визуализации
    images = images.cpu()
    labels = labels.cpu()
    predictions = predictions.cpu()

    plt.figure(figsize=(15, 10))
    for i in range(12):
        plt.subplot(3, 4, i + 1)
        imshow(images[i])

        predicted_label = predictions[i].item()
        true_label = labels[i].item()

        color = 'green' if predicted_label == true_label else 'red'

        plt.title(f'Предсказано: {class_names[predicted_label]}\n'
                  f'Реальное: {class_names[true_label]}',
                  color=color, fontsize=10)

    plt.tight_layout()
    plt.show()

    # Графики обучения
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs + 1), train_losses, 'b-', label='Потери')
    plt.xlabel('Эпохи')
    plt.ylabel('Потери')
    plt.title('Потери во время обучения')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs + 1), train_accuracies, 'r-', label='Точность')
    plt.xlabel('Эпохи')
    plt.ylabel('Точность (%)')
    plt.title('Точность во время обучения')
    plt.legend()

    plt.tight_layout()
    plt.show()
