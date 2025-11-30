````markdown
# Trading Journal · Шпаргалка по статистике (с маржей в USDT)

Проект: `trading_journal` на WSL  
Цель: добавить **статистику по сделкам** + колонку **Маржа (USDT)** и **Номинал (USDT)**.

Итог:

- поле `quantity` = **маржа в USDT**;
- на главной странице:
  - Winrate, суммарный/средний PnL;
  - лучшая/худшая сделка;
  - PnL по LONG/SHORT;
  - таблица сделок с номиналом позиции.

---

## 1. Модель Trade (маржа + номинал)

**Файл:** `journal/models.py`  
**Путь:** `C:\Users\cp24\Documents\django\trading_journal\journal\models.py`

Полный код модели (можно целиком заменить):

```python
from django.db import models


class Trade(models.Model):
    SIDE_CHOICES = [
        ("LONG", "Long"),
        ("SHORT", "Short"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Открыта"),
        ("CLOSED", "Закрыта"),
    ]

    exchange = models.CharField(
        max_length=50,
        default="Binance",
        verbose_name="Биржа",
    )
    symbol = models.CharField(
        max_length=20,
        verbose_name="Пара (например, BTCUSDT)",
    )
    side = models.CharField(
        max_length=5,
        choices=SIDE_CHOICES,
        verbose_name="Направление",
    )
    leverage = models.PositiveIntegerField(
        default=1,
        verbose_name="Плечо",
    )
    quantity = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Маржа (USDT)",
        help_text="Сколько маржи в USDT выделено под эту сделку.",
    )
    entry_price = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        verbose_name="Цена входа",
    )
    stop_loss = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Stop-loss",
    )
    take_profit_1 = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="TP1",
    )
    take_profit_2 = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="TP2",
    )
    take_profit_3 = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="TP3",
    )

    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default="OPEN",
        verbose_name="Статус",
    )
    realized_pnl = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Результат (USDT)",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Закрыто",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
    )

    @property
    def position_notional(self):
        """Номинал позиции (объём) = маржа * плечо в USDT."""
        if self.quantity is None or self.leverage is None:
            return None
        return self.quantity * self.leverage

    def __str__(self):
        return f"{self.symbol} {self.side} @ {self.entry_price}"

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
        ordering = ["-created_at"]
````

### Миграции (опционально)

**WSL-команды:**

```bash
cd /mnt/c/Users/cp24/Documents/django/trading_journal
source .venv/bin/activate

python manage.py makemigrations
python manage.py migrate
```

---

## 2. View с расчётом статистики

**Файл:** `journal/views.py`  
**Путь:** `C:\Users\cp24\Documents\django\trading_journal\journal\views.py`

Полный код:

```python
from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Trade


def trades_list(request):
    trades = Trade.objects.all()

    # Закрытые сделки (там, где PnL уже посчитан)
    closed = trades.exclude(realized_pnl__isnull=True)

    total_trades = trades.count()
    total_closed = closed.count()
    total_open = trades.filter(status="OPEN").count()

    wins = closed.filter(realized_pnl__gt=0)
    losses = closed.filter(realized_pnl__lt=0)
    breakevens = closed.filter(realized_pnl=0)

    pnl_sum = closed.aggregate(s=Sum("realized_pnl"))["s"] or 0
    avg_pnl = pnl_sum / total_closed if total_closed > 0 else 0

    win_count = wins.count()
    loss_count = losses.count()

    winrate = (win_count / total_closed * 100) if total_closed > 0 else 0

    best_trade = closed.order_by("-realized_pnl").first()
    worst_trade = closed.order_by("realized_pnl").first()

    # PnL по направлению (LONG / SHORT)
    pnl_by_side = (
        closed
        .values("side")
        .annotate(
            total_pnl=Sum("realized_pnl"),
            count=Count("id"),
        )
        .order_by("side")
    )

    stats = {
        "total_trades": total_trades,
        "total_closed": total_closed,
        "total_open": total_open,
        "wins": win_count,
        "losses": loss_count,
        "breakevens": breakevens.count(),
        "pnl_sum": pnl_sum,
        "avg_pnl": avg_pnl,
        "winrate": winrate,
        "best_trade": best_trade,
        "worst_trade": worst_trade,
        "pnl_by_side": list(pnl_by_side),
    }

    context = {
        "trades": trades,
        "stats": stats,
    }
    return render(request, "trades_list.html", context)
```

---

## 3. Шаблон trades_list.html (карточки статистики + таблица)

**Файл:** `templates/trades_list.html`  
**Путь:** `C:\Users\cp24\Documents\django\trading_journal\templates\trades_list.html`

Полный шаблон с уже исправленным полем **Маржа (USDT)** и колонкой **Номинал (USDT)**:

```html
{% extends "base.html" %}

{% block title %}Журнал сделок · Trading Journal{% endblock %}

{% block content %}
<div class="card card-dark mb-4">
    <div class="card-body">
        <div class="d-flex justify-content-between flex-wrap gap-3">
            <div>
                <h1 class="h4 mb-2">Журнал сделок</h1>
                <p class="text-secondary mb-0">
                    Все сделки из базы данных Django. Новые сделки добавляются через <a href="/admin/">админ-панель</a>.
                </p>
            </div>
            {% if stats %}
            <div class="text-end">
                <div class="fw-semibold">Всего сделок: {{ stats.total_trades }}</div>
                <div class="text-secondary small">
                    Закрытых: {{ stats.total_closed }} · Открытых: {{ stats.total_open }}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>

{% if stats %}
<div class="row mb-4 g-3">
    <!-- Winrate & PnL -->
    <div class="col-md-4">
        <div class="card card-dark h-100">
            <div class="card-body">
                <h2 class="h6 text-secondary text-uppercase mb-2">Winrate &amp; PnL</h2>
                <p class="mb-1">
                    Winrate:
                    <strong>{{ stats.winrate|floatformat:1 }}%</strong>
                </p>
                <p class="mb-1">
                    Побед: <span class="text-success">{{ stats.wins }}</span>,
                    поражений: <span class="text-danger">{{ stats.losses }}</span>,
                    0: {{ stats.breakevens }}
                </p>
                <p class="mb-1">
                    Суммарный PnL:
                    {% if stats.pnl_sum > 0 %}
                        <span class="pnl-positive">+{{ stats.pnl_sum }}</span>
                    {% elif stats.pnl_sum < 0 %}
                        <span class="pnl-negative">{{ stats.pnl_sum }}</span>
                    {% else %}
                        {{ stats.pnl_sum }}
                    {% endif %}
                </p>
                <p class="mb-0">
                    Средний PnL на сделку:
                    {% if stats.avg_pnl > 0 %}
                        <span class="pnl-positive">+{{ stats.avg_pnl|floatformat:2 }}</span>
                    {% elif stats.avg_pnl < 0 %}
                        <span class="pnl-negative">{{ stats.avg_pnl|floatformat:2 }}</span>
                    {% else %}
                        {{ stats.avg_pnl|floatformat:2 }}
                    {% endif %}
                </p>
            </div>
        </div>
    </div>

    <!-- Лучшие / худшие сделки -->
    <div class="col-md-4">
        <div class="card card-dark h-100">
            <div class="card-body">
                <h2 class="h6 text-secondary text-uppercase mb-2">Лучшие / худшие сделки</h2>
                {% if stats.best_trade %}
                    <p class="mb-1">
                        <span class="text-secondary small">Лучшая:</span><br>
                        {{ stats.best_trade.created_at|date:"d.m.Y H:i" }},
                        {{ stats.best_trade.symbol }}
                        ({{ stats.best_trade.side }}) –
                        <span class="pnl-positive">+{{ stats.best_trade.realized_pnl }}</span>
                    </p>
                {% else %}
                    <p class="mb-1 text-secondary">Лучшая: —</p>
                {% endif %}

                {% if stats.worst_trade %}
                    <p class="mb-0 mt-2">
                        <span class="text-secondary small">Худшая:</span><br>
                        {{ stats.worst_trade.created_at|date:"d.m.Y H:i" }},
                        {{ stats.worst_trade.symbol }}
                        ({{ stats.worst_trade.side }}) –
                        <span class="pnl-negative">{{ stats.worst_trade.realized_pnl }}</span>
                    </p>
                {% else %}
                    <p class="mb-0 text-secondary">Худшая: —</p>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- PnL по направлению -->
    <div class="col-md-4">
        <div class="card card-dark h-100">
            <div class="card-body">
                <h2 class="h6 text-secondary text-uppercase mb-2">PnL по направлению</h2>
                {% if stats.pnl_by_side %}
                    <ul class="list-unstyled mb-0">
                        {% for row in stats.pnl_by_side %}
                            <li class="mb-1">
                                {% if row.side == "LONG" %}
                                    <span class="badge badge-long me-1">LONG</span>
                                {% else %}
                                    <span class="badge badge-short me-1">SHORT</span>
                                {% endif %}
                                сделок: {{ row.count }},
                                PnL:
                                {% if row.total_pnl > 0 %}
                                    <span class="pnl-positive">+{{ row.total_pnl }}</span>
                                {% elif row.total_pnl < 0 %}
                                    <span class="pnl-negative">{{ row.total_pnl }}</span>
                                {% else %}
                                    {{ row.total_pnl }}
                                {% endif %}
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p class="mb-0 text-secondary">Пока нет закрытых сделок с PnL.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endif %}

{% if trades %}
<div class="card card-dark">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-dark table-hover mb-0 align-middle">
                <thead>
                <tr>
                    <th scope="col">Дата</th>
                    <th scope="col">Биржа</th>
                    <th scope="col">Пара</th>
                    <th scope="col">Напр.</th>
                    <th scope="col">Плечо</th>
                    <th scope="col">Маржа (USDT)</th>
                    <th scope="col">Номинал (USDT)</th>
                    <th scope="col">Вход</th>
                    <th scope="col">SL</th>
                    <th scope="col">TP1/TP2/TP3</th>
                    <th scope="col">Статус</th>
                    <th scope="col">P&amp;L (USDT)</th>
                    <th scope="col">Комментарий</th>
                </tr>
                </thead>
                <tbody>
                {% for trade in trades %}
                    <tr>
                        <td>{{ trade.created_at|date:"d.m.Y" }}<br>{{ trade.created_at|date:"H:i" }}</td>
                        <td>{{ trade.exchange }}</td>
                        <td>{{ trade.symbol }}</td>
                        <td>
                            {% if trade.side == "LONG" %}
                                <span class="badge badge-long">LONG</span>
                            {% else %}
                                <span class="badge badge-short">SHORT</span>
                            {% endif %}
                        </td>
                        <td>{{ trade.leverage }}x</td>
                        <td>{{ trade.quantity }}</td>
                        <td>
                            {% if trade.position_notional %}
                                {{ trade.position_notional }}
                            {% else %}
                                —
                            {% endif %}
                        </td>
                        <td>{{ trade.entry_price }}</td>
                        <td>
                            {% if trade.stop_loss %}
                                {{ trade.stop_loss }}
                            {% else %}
                                —
                            {% endif %}
                        </td>
                        <td>
                            {% if trade.take_profit_1 %}TP1: {{ trade.take_profit_1 }}{% endif %}
                            {% if trade.take_profit_2 %}<br>TP2: {{ trade.take_profit_2 }}{% endif %}
                            {% if trade.take_profit_3 %}<br>TP3: {{ trade.take_profit_3 }}{% endif %}
                            {% if not trade.take_profit_1 and not trade.take_profit_2 and not trade.take_profit_3 %}
                                —
                            {% endif %}
                        </td>
                        <td>{{ trade.get_status_display }}</td>
                        <td>
                            {% if trade.realized_pnl %}
                                {% if trade.realized_pnl > 0 %}
                                    <span class="pnl-positive">+{{ trade.realized_pnl }}</span>
                                {% elif trade.realized_pnl < 0 %}
                                    <span class="pnl-negative">{{ trade.realized_pnl }}</span>
                                {% else %}
                                    {{ trade.realized_pnl }}
                                {% endif %}
                            {% else %}
                                {% if trade.status == "OPEN" %}
                                    <span class="text-secondary">Открыта</span>
                                {% else %}
                                    —
                                {% endif %}
                            {% endif %}
                        </td>
                        <td style="max-width: 220px; white-space: pre-wrap;">
                            {{ trade.comment|default:"" }}
                        </td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% else %}
<div class="card card-dark">
    <div class="card-body">
        <p class="mb-0">
            Пока нет ни одной сделки. Зайди в <a href="/admin/">админку</a> и создай первую.
        </p>
    </div>
</div>
{% endif %}
{% endblock %}
```

---

## 4. Запуск и проверка

**WSL-команды:**

```bash
cd /mnt/c/Users/cp24/Documents/django/trading_journal
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8002
```

Браузер (Windows):

- Журнал + статистика: [http://localhost:8002/](http://localhost:8002/)
    
- Админка: [http://localhost:8002/admin/](http://localhost:8002/admin/)
    

---

### Мини-чеклист

```text
1) models.py:
   - quantity → "Маржа (USDT)"
   - добавлено свойство position_notional

2) views.py:
   - trades_list считает stats (winrate, PnL, лучшая/худшая, PnL по side)

3) trades_list.html:
   - сверху 3 карточки статистики
   - в таблице: Маржа (USDT) + Номинал (USDT)
   - PnL подсвечивается зелёным/красным

4) Данные вводим через /admin/ → JOURNAL → Сделки
```

#django #trading #journal #stats #маржа #usdt #wsl #шпаргалка

```
::contentReference[oaicite:0]{index=0}
```