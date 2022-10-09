PrivatBank online synchronization
=======================

Модуль выгружает банковские выписки с PrivatBank в Odoo, а также загружает счета на оплату с Odoo в PrivatBank.


Инструкция:
-----------------

1. Создать Журнал с Аутоклиент id и токеном, `Инструкция по работе с приложением «Автоклиент»
<https://docs.google.com/document/d/e/2PACX-1vTion-fu1RzMCQgZXOYKKWAmvi-QAAxZ7AKnAZESGY5lF2j3nX61RBsa5kXzpu7t5gacl6TgztonrIE/pub>`_.

-----------------------

.. image:: account_p24_sync/static/description/screenshot01.png
  :width: 1000
  :alt: Screenshot

-----------------------

2. Выбрать метод оплаты Privat24

.. image:: account_p24_sync/static/description/screenshot02.png
  :width: 1000
  :alt: Screenshot

-----------------------

3. При  нажатии кнопки "P24 Sync" Открывается визард с выбором диапазона дат с которого будет производиться выгрузка банковских выписок

.. image:: account_p24_sync/static/description/screenshot03.png
  :width: 1000
  :alt: Screenshot

-----------------------

4. После удачной выгрузки они будут показаны автоматически

.. image:: account_p24_sync/static/description/screenshot04.png
  :width: 1000
  :alt: Screenshot

-----------------------

5. Также можна загружать оплаты по счёту в ПриватБанк, для этого нужно выбрать журнал и метод оплаты при регистрации платежа в счёте-фактуре

.. image:: account_p24_sync/static/description/screenshot05.png
  :width: 1000
  :alt: Screenshot

-----------------------

6. В account payment появится кнопка для экспорта

.. image:: account_p24_sync/static/description/screenshot06.png
  :width: 1000
  :alt: Screenshot


Ссылка на API
-------------

`Опис API для взаємодії з серверною частиною Автоклієнта версія 3.0.0
<https://docs.google.com/document/d/e/2PACX-1vTtKvGa3P4E-lDqLg3bHRF6Wi9S7GIjSMFEFxII5qQZBGxuTXs25hQNiUU1hMZQhOyx6BNvIZ1bVKSr/pub>`_.
