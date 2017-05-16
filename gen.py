#!/usr/bin/env python3

import faker
import random
import datetime
import sys
import os

import xml.etree.ElementTree as ET
from xml.dom import minidom

fake = faker.Factory.create()
fake_local = faker.Factory.create('ru_RU')

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def val(top, path, obj_value, tooltip_ru, tooltip_en, name_ru, name_en):
    child = top
    for p in path.split('.'):
        if child.find(p):
            child = child.find(p)
        else:
            child = ET.SubElement(child, p)

    e = ET.SubElement(child, 'TooltipName')
    e.text = tooltip_ru

    e = ET.SubElement(child, 'TooltipNameEng')
    e.text = tooltip_en

    e = ET.SubElement(child, 'ParameterName')
    e.text = name_ru

    e = ET.SubElement(child, 'ParameterNameEng')
    e.text = name_en


    if isinstance(obj_value, str):
        e = ET.SubElement(child, 'Type')
        e.text = "String"

        e = ET.SubElement(child, 'Value')
        e.text = obj_value
    elif isinstance(obj_value, int):
        e = ET.SubElement(child, 'Type')
        e.text = "Integer"

        e = ET.SubElement(child, 'Value')
        e.text = str(obj_value)
    elif isinstance(obj_value, float):
        e = ET.SubElement(child, 'Type')
        e.text = "Double"

        e = ET.SubElement(child, 'Value')
        e.text = str(obj_value)
    elif isinstance(obj_value, bool):
        e = ET.SubElement(child, 'Type')
        e.text = "Boolean"

        e = ET.SubElement(child, 'Value')
        e.text = {True: "true", False: "false"}[obj_value]

    elif isinstance(obj_value, bool):
        e = ET.SubElement(child, 'Type')
        e.text = "Boolean"

        e = ET.SubElement(child, 'Value')
        e.text = {True: "true", False: "false"}[obj_value]

    elif isinstance(obj_value, datetime.date):
        e = ET.SubElement(child, 'Type')
        e.text = "DateTime"

        e = ET.SubElement(child, 'Value')
        e.text = obj_value.isoformat()


def generate_fx():
    top = ET.Element('body')

    val(top, 'ObjModelUID', fake_local.md5(),
        'Универсальный идентификатор объектной модели',
        'Object Model Universal ID',
        'Универсальный ID объектной модели',
        'Object Model Universal ID')

    val(top, 'ObjType', 'Trade',
        'Тип бизнес-объекта',
        'Business-object type',
        'Тип бизнес-объекта',
        'Business-object type')

    val(top, 'ObjUID', fake_local.uuid4(),
        'Универсальный идентификатор объекта',
        'Business-object Universal ID',
        'Универсальный ID бизнес-объекта',
        'Business-object Universal ID')

    val(top, 'RootObjType', '',
        'Тип бизнес-объекта верхнего уровня',
        'Root business-object type',
        'Тип породившего бизнес-объекта ',
        'Root business-object Type')

    val(top, 'RootObjUID', fake.uuid4(),
        'Универсальный идентификатор объекта верхнего уровня',
        'Root business-object universal ID',
        'Универсальный ID  породившего бизнес-объекта',
        'Root business-object universal ID')

    val(top, 'OriginSystem', fake.bs(),
        'Система происхождения',
        'Origin System',
        'Система происхождения',
        'Origin System')

    val(top, 'OriginSystemID', fake_local.uuid4(),
        'Идентификатор объекта в системе происхождения',
        'Business-object Origin System ID',
        'ID объекта в системе происхождения',
        'Business-object Origin System ID')

    val(top, 'RegDateTime', fake_local.date_time_this_month(before_now=True),
        'Дата и время регистрации',
        'Registration date and time ',
        'Дата и время регистрации',
        'Registration Date and Time')

    val(top, 'BusinessEventType', 'Trade',
        'Тип сделки',
        'Business-event type',
        'Тип бизн.-события',
        'Bus. Event Type')

    val(top, 'EventDateTime', fake_local.date_time_this_month(before_now=True),
        'Дата и время события',
        'Event Date and Time',
        'Дата и время события',
        'Event Date and Time')

    val(top, 'Сomment', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Комментарий',
        'Сomment',
        'Комментарий',
        'Сomment')

    val(top, 'TradeType', 'FX',
        'Тип сделки',
        'Trade type',
        'Тип сделки',
        'TradeType')

    val(top, 'TradeFloorType', fake_local.pybool(),
        'Тип торговой площадки',
        'Trade Floor Type',
        'Тип торг. площадки',
        'Trade floor type')

    val(top, 'MasterAgreement.RootProductUID', fake_local.uuid4(),
        'Универсальный идентификатор объекта Ген. Соглашения',
        'Master Agreement Universal ID',
        'Универсальный ID объекта Ген. Соглашения',
        'Master Agreement Universal ID')

    val(top, 'MasterAgreement.MasterAgreementNumber', fake_local.pyint(),
        'Номер ген соглашения',
        'Master Agreement Number',
        'Номер ген соглашения',
        'General agreement number')

    val(top, 'MasterAgreement.WithoutMasterAgreement', fake_local.pybool(),
        'Сделка без ГС',
        'Without Master Agreement',
        'Сделка без ГС',
        'Without Master Agreement')

    val(top, 'Participants.Buyer.BuyerNickName', fake_local.profile()['username'],
        'Покупатель',
        'Buyer',
        'Покупатель',
        'Buyer')

    val(top, 'Participants.Seller.SellerNickName', fake_local.profile()['username'],
        'Продавец',
        'Seller',
        'Продавец',
        'Seller')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyersBranch', fake.bs(),
        'Подразделение Покупателя',
        'Buyer\'s Branch',
        'Подразделение Покупателя',
        'Buyer\'s Branch')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerProfitCenter', fake.bs(),
        'Профит-центр Покупателя',
        'Buyer\'s Profit center',
        'Профит-центр Покупателя',
        'Buyer\'s Profit center')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerPortfolio', fake.bs(),
        'Портфель Покупателя',
        'Buyer\'s Portfolio',
        'Портфель Покупателя',
        'Buyer\'s Portfolio')

    val(top, 'Participants.Seller.AccountingRegisters.SellersBranch', fake.bs(),
        'Подразделение Продавца',
        'Seller\'s Branch',
        'Подразделение Продавца',
        'Seller\'s Branch')

    val(top, 'Participants.Seller.AccountingRegisters.SellerProfitCenter', fake.bs(),
        'Профит-центр Продавца',
        'Seller\'s Profit center',
        'Профит-центр Продавца',
        'Seller\'s Profit center')

    val(top, 'Participants.Seller.AccountingRegisters.SellerPortfolio', fake.bs(),
        'Портфель Продавца',
        'Seller\'s Portfolio',
        'Портфель Продавца',
        'Seller\'s Portfolio')

    val(top, 'Participants.Trader.TraderName', fake_local.name(),
        'Имя Трейдера со стороны Продавца',
        'Trader Name',
        'Имя Трейдера',
        'Trader Name')

    val(top, 'EventDetails.DealType', {True: 'Buy', False: 'Sell'}[fake_local.pybool()],
        'Тип сделки',
        'Deal Type',
        'Тип сделки',
        'Deal Type')

    val(top, 'EventDetails.NearLeg.TradeDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата сделки',
        'Trade Date',
        'Дата сделки',
        'Trade Date')

    val(top, 'EventDetails.NearLeg.ValueDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата валютирования',
        'Value Date',
        'Дата валютирования',
        'Value Date')

    val(top, 'EventDetails.NearLeg.Currency1', fake_local.currency_code(),
        'Код валюты 1',
        'Currency1',
        'Код валюты 1',
        'Currency1')

    val(top, 'EventDetails.NearLeg.Currency1Amount', fake_local.pyfloat(left_digits=5, right_digits=2, positive=True),
        'Сумма валюты 1',
        'Currency1Amount',
        'Сумма валюты 1',
        'Currency1Amount')

    val(top, 'EventDetails.NearLeg.Currency2', fake_local.currency_code(),
        'Код валюты 2 ',
        'Currency2',
        'Код валюты 2 ',
        'Currency2')

    val(top, 'EventDetails.NearLeg.Currency2Amount', fake_local.pyfloat(left_digits=5, right_digits=2, positive=True),
        'Сумма валюты 2',
        'Currency2Amount',
        'Сумма валюты 2',
        'Currency2Amount')

    val(top, 'EventDetails.NearLeg.rate', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Курс ',
        'Rate',
        'Курс ',
        'Rate')

    val(top, 'EventDetails.NearLeg.exchangedCurrency', fake_local.currency_code(),
        'Код котируемой валюты',
        'exchangedCurrency',
        'Код котируемой валюты',
        'exchangedCurrency')

    val(top, 'EventDetails.FarLeg.ValueDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата валютирования',
        'Value Date',
        'Дата валютирования',
        'Value Date')

    val(top, 'EventDetails.FarLeg.Currency1', fake_local.currency_code(),
        'Код валюты 1',
        'Currency1',
        'Код валюты 1',
        'Currency1')

    val(top, 'EventDetails.FarLeg.Currency1Amount', fake_local.pyfloat(left_digits=5, right_digits=2, positive=True),
        'Сумма валюты 1',
        'Currency1Amount',
        'Сумма валюты 1',
        'Currency1Amount')

    val(top, 'EventDetails.FarLeg.Currency2', fake_local.currency_code(),
        'Код валюты 2 ',
        'Currency2',
        'Код валюты 2 ',
        'Currency2')

    val(top, 'EventDetails.FarLeg.Currency2Amount', fake_local.pyfloat(left_digits=5, right_digits=2, positive=True),
        'Сумма валюты 2',
        'Currency2Amount',
        'Сумма валюты 2',
        'Currency2Amount')

    val(top, 'EventDetails.FarLeg.rate', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Курс ',
        'Rate',
        'Курс ',
        'Rate')

    val(top, 'EventDetails.FarLeg.exchangedCurrency', fake_local.currency_code(),
        'Код котируемой валюты',
        'exchangedCurrency',
        'Код котируемой валюты',
        'exchangedCurrency')

    return prettify(top)

def generate_fx_fwd():
    top = ET.Element('body')

    val(top, 'ObjModelUID', fake_local.md5(),
        'Универсальный идентификатор объектной модели',
        'Object Model Universal ID',
        'Универсальный ID объектной модел',
        'Object Model Universal ID')

    val(top, 'ObjType', 'Trade',
        'Тип бизнес-объекта',
        'Business-object type',
        'Тип бизнес-объекта',
        'Business-object Type')

    val(top, 'ObjUID', fake_local.uuid4(),
        'Универсальный идентификатор объекта',
        'Business-object Universal ID',
        'Универсальный ID бизнес-объекта',
        'Business-object Universal ID')

    val(top, 'RootObjType', '',
        'Тип бизнес-объекта верхнего уровня',
        'Root business-object type',
        'Тип породившего бизнес-объекта ',
        'Root business-object Type')

    val(top, 'RootObjUID', fake.uuid4(),
        'Универсальный идентификатор объекта верхнего уровня',
        'Root business-object universal ID',
        'Универсальный ID  породившего бизнес-объекта',
        'Root business-object universal ID')

    val(top, 'OriginSystem', fake.bs(),
        'Система происхождения',
        'Origin System',
        'Система происхождения',
        'Origin System')

    val(top, 'OriginSystemID', fake_local.uuid4(),
        'Идентификатор объекта в системе происхождения',
        'Business-object Origin System ID',
        'ID объекта в системе происхождения',
        'Business-object Origin System ID')

    val(top, 'RegDateTime', fake_local.date_time_this_month(before_now=True),
        'Дата и время регистрации',
        'Registration date and time ',
        'Дата и время регистрации',
        'Registration Date and Time')

    val(top, 'BusinessEventType', 'Trade',
        'Тип сделки',
        'Business-event type',
        'Тип бизн.-события',
        'Bus. Event Type')

    val(top, 'EventDateTime', fake_local.date_time_this_month(before_now=True),
        'Дата и время события',
        'Event Date and Time',
        'Дата и время события',
        'Event Date and Time')

    val(top, 'Сomment', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Комментарий',
        'Сomment',
        'Комментарий',
        'Сomment')

    val(top, 'TradeType', 'FWD FX',
        'Тип сделки',
        'Trade type',
        'Тип сделки',
        'TradeType')

    val(top, 'TradeFloorType', fake_local.pybool(),
        'Тип торговой площадки',
        'Trade Floor Type',
        'Тип торг. площадки',
        'Trade floor type')

    val(top, 'MasterAgreement.RootProductUID', fake_local.uuid4(),
        'Универсальный идентификатор объекта Ген. Соглашения',
        'Master Agreement Universal ID',
        'Универсальный ID объекта Ген. Соглашения',
        'Master Agreement Universal ID')

    val(top, 'MasterAgreement.MasterAgreementNumber', fake_local.pyint(),
        'Номер ген соглашения',
        'Master Agreement Number',
        'Номер ген соглашения',
        'General agreement number')

    val(top, 'MasterAgreement.WithoutMasterAgreement', fake_local.pybool(),
        'Сделка без ГС',
        'Without Master Agreement',
        'Сделка без ГС',
        'Without Master Agreement')

    val(top, 'EventDetails.CorpPaymAsCashFlow', fake_local.pybool(),
        'Поле, которое показывает встраивается ли купон в сделку, либо должен быть выплачен контрагенту',
        'Return corporate payments as cashflow or write off the debt',
        'Корп. выпл.: возврат платежом',
        'Corp. Paym: as CashFlow')

    val(top, 'Participants.Buyer.BuyerNickName', fake_local.profile()['username'],
        'Покупатель',
        'Buyer',
        'Покупатель',
        'Buyer')

    val(top, 'Participants.Seller.SellerNickName', fake_local.profile()['username'],
        'Продавец',
        'Seller',
        'Продавец',
        'Seller')

    val(top, 'Participants.Buyer.LegalEntity.BuyerLegalEntity', fake_local.company(),
        'Юр. Лицо Покупателя',
        'Buyer Legal Entity',
        'Юр. Лицо Покупателя',
        'Buyer LE')

    val(top, 'Participants.Seller.LegalEntity.SellerLegalEntity', fake_local.company(),
        'Юр. Лицо Продавца  ',
        'Seller Legal Entity',
        'Юр. Лицо Продавца  ',
        'Seller LE')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyersBranch', fake.bs(),
        'Подразделение Покупателя',
        'Buyer\'s Branch',
        'Подразделение Покупателя',
        'Buyer\'s Branch')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerProfitCenter', fake.bs(),
        'Профит-центр Покупателя',
        'Buyer\'s Profit center',
        'Профит-центр Покупателя',
        'Buyer\'s Profit center')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerPortfolio', fake.bs(),
        'Портфель Покупателя',
        'Buyer\'s Portfolio',
        'Портфель Покупателя',
        'Buyer\'s Portfolio')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerBook', fake.uuid4(),
        'Книга Покупателя',
        'Buyer\'s Book',
        'Книга Покупателя',
        'Buyer\'s Book')

    val(top, 'Participants.Seller.AccountingRegisters.SellersBranch', fake.uuid4(),
        'Подразделение Продавца',
        'Seller\'s Branch',
        'Подразделение Продавца',
        'Seller\'s Branch')

    val(top, 'Participants.Seller.AccountingRegisters.SellerProfitCenter', fake.uuid4(),
        'Профит-центр Продавца',
        'Seller\'s Profit center',
        'Профит-центр Продавца',
        'Seller\'s Profit center')

    val(top, 'Participants.Seller.AccountingRegisters.SellerPortfolio', fake.uuid4(),
        'Портфель Продавца',
        'Seller\'s Portfolio',
        'Портфель Продавца',
        'Seller\'s Portfolio')

    val(top, 'Participants.Seller.AccountingRegisters.SellerBook', fake.uuid4(),
        'Книга Продавца',
        'Seller\'s Book',
        'Книга Продавца',
        'Seller\'s Book')

    val(top, 'Participants.Buyer.BuyersTraderName', fake_local.name(),
        'Имя Трейдера со стороны Покупателя',
        'Buyer\'s Trader Name',
        'Имя Трейдера (Пок.)',
        'Buyer\'s Trader Name')

    val(top, 'Participants.Seller.SellersTraderName', fake_local.name(),
        'Имя Трейдера со стороны Продавца',
        'Seller\'s Trader Name',
        'Имя Трейдера (Прод.)',
        'Seller\'s Trader Name')

    val(top, 'EventDetails.TradeDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата сделки',
        'Trade Date',
        'Дата сделки',
        'Trade Date')

    val(top, 'EventDetails.MaturityType', 'None',
        'Срочность сделки',
        'Maturity Type',
        'Срочность сделки',
        'Maturity Type')

    val(top, 'EventDetails.MaturityDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата завершения обязательств по сделке',
        'Maturity Date',
        'Дата завершения',
        'Maturity Date')

    val(top, 'EventDetails.SettlementMode', 'On foot',
        'Способ поставки',
        'Settlement Mode',
        'Способ поставки',
        'Settlement Mode')

    val(top, 'EventDetails.DealingCcy', fake_local.currency_code(),
        'Дилинговая валюта',
        'Dealing Ccy',
        'Дилинговая валюта',
        'Dealing Ccy')

    val(top, 'EventDetails.PricingCcy', fake_local.currency_code(),
        'Прайсинговая валюта',
        'Pricing Ccy',
        'Прайсинговая валюта',
        'Pricing Ccy')

    val(top, 'EventDetails.UnderlyingType', fake.sentence(nb_words=2),
        'Тип базового актива',
        'Underlying Type',
        'Тип инструмента',
        'Underlying Type')

    val(top, 'EventDetails.UnderlyingUID', fake.uuid4(),
        'Универсальный идентификатор базового актива',
        'Underlying asset universal ID',
        '-',
        '-')

    val(top, 'EventDetails.Underlying', fake.sentence(nb_words=2),
        'Базовый актив',
        'Underlying asset',
        'Инструмент',
        'Underlying')

    val(top, 'EventDetails.ISIN', fake.uuid4(),
        'ISIN',
        'ISIN',
        'ISIN',
        'ISIN')

    val(top, 'EventDetails.DomesticCode', fake.pyint(),
        'Национальный код инструмента',
        'Underlying Domestic Code',
        'Национальный код инструмента',
        'Underlying Domestic Code')

    val(top, 'EventDetails.UnderlyingCcy', fake.currency_code(),
        'Валюта номинала',
        'Underlying сurrency',
        'Валюта инструмента',
        'Instrument Ccy')

    val(top, 'EventDetails.UnderlyingQty', fake.pyint() % 5000,
        'Количество базового актива',
        'Quantity of Underlying Asset',
        'Количество ',
        'Quantity')

    val(top, 'EventDetails.QuantityUnits', 'Units',
        'Единицы номингирования (в чем выражается количество)',
        'Quantity units',
        '-',
        '-')

    val(top, 'EventDetails.TradePrice', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Цена заключения сделки за единицу базового актива в валюте переоценки ',
        'Trade price per the unit of Underlying Asset',
        'Цена заключения сделки',
        'Trade Price in Trade Pricing Ccy per the unit of Underlying Asset')

    val(top, 'EventDetails.QuoteUnits', 'None',
        'Единицы переоценки ',
        'Quote Units',
        'Единицы переоценки',
        'Quote Units')

    val(top, 'EventDetails.UnderlyingValueUnderlyingCcy', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Эквивалентная стоимость базового актива в валюте номинала',
        'Underluying asset value in underlying currency',
        'Стоим. Баз. актива в валюте номинала',
        'Value in Pricing Ccy')

    val(top, 'EventDetails.PaymentCcy', fake.currency_code(),
        'Валюта расчетов по сделке',
        'Payment Ccy',
        'Вал. расч. ',
        'Paym. Ccy')

    val(top, 'EventDetails.CnvRateUnderlCcyPaymCcy', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Курс конвертации из валюты базового актива в валюту расчетов.',
        'Rate to convert from Underluying Ccy to  Payment Ccy',
        'Курс. Конв. ([CcyPair])',
        'Cnv. Rate ([CcyPair])')

    val(top, 'EventDetails.CnvCcyPairUnderlCcyPaymCcy', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Валютная пара валюты базового актива и валюты расчетов',
        'Ccy Pair for Underluying Ccy and Payment Ccy',
        '-',
        '-')

    val(top, 'EventDetails.AmountDuePaymCcy', fake_local.pyfloat(left_digits=5, right_digits=2, positive=True),
        'Сумма к выплате в валюте расчетов',
        'Amount Due in payment currency',
        'Сумма к выпл. в вал. расч.',
        'Amount Due in Paym. Ccy')

    val(top, 'SettlementConditions.DeliveryTerms', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Последовательность поставки',
        'Delivery Terms',
        'Последовательность поставки',
        'Delivery Terms')

    val(top, 'SettlementConditions.ValueDateDealingCcy', fake_local.date_time_this_month(before_now=True),
        'Дата платежа по дилинговой валюте',
        'Value Date for Dealing Ccy',
        'Дата оплаты([DealingCcy])',
        'Value Date ([ DealingCcy])')

    val(top, 'SettlementConditions.ValueDatePricingCcy', fake_local.date_time_this_month(before_now=True),
        'Дата платежа по прайсинговой валюте',
        'Value Date for Pricing Ccy',
        'Дата платежа([PricingCcy])',
        'Value Date ([ PricingCcy])')

    val(top, 'SettlementConditions.RuleToDefineStandardValueDate', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Правило определения стандартной даты расчетов',
        'Rule to define standard value date',
        'Правило определения стандартной даты расчетов',
        'Rule to Define Std. Val. Date')

    val(top, 'SettlementConditions.HolidaysCalendar', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Календарь праздников и выходных дат. Задается в форме перечня активов, расписание праздников по которым требуется включить в календарь сделки.',
        'Holidays calendar. Calendar is set as a list of assets whose holidays schedules should be included to the calendar of the deal',
        'Календарь праздн. И вых. Дней',
        'Holidays Calendar')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientsBranch', fake.bs(),
        'Подразделение Получателя платежа',
        'Cashflow recepient\'s Branch',
        'Подразделение Получателя платежа',
        'Recepient\'s Branch')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientProfitCenter', fake.bs(),
        'Профит-центр Получателя платежа',
        'Cashflow recepient\'s Profit center',
        'Профит-центр Получателя платежа',
        'Recepient\'s Profit center')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientPortfolio', fake.uuid4(),
        'Портфель Получателя платежа',
        'Cashflow recepient\'s Portfolio',
        'Портфель Получателя платежа',
        'Recepient\'s Portfolio')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientBook', fake.uuid4(),
        'Книга Получателя платежа',
        'Cashflow recepient\'s Book',
        'Книга Получателя платежа',
        'Recepient\'s Book')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayersBranch', fake.uuid4(),
        'Подразделение Отправителя платежа',
        'Cashflow payer\'s Branch',
        'Подразделение Отправителя платежа',
        'Payer\'s Branch')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayerProfitCenter', fake.bs(),
        'Профит-центр Отправителя платежа',
        'Cashflow payer\'s Profit center',
        'Профит-центр Отправителя платежа',
        'Payer\'s Profit center')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayerPortfolio', fake.uuid4(),
        'Портфель Отправителя платежа',
        'Cashflow payer\'s Portfolio',
        'Портфель Отправителя платежа',
        'Payer\'s Portfolio')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayerBook', fake.uuid4(),
        'Книга Отправителя платежа',
        'Cashflow payer\'s Book',
        'Книга Отправителя платежа',
        'Payer\'s Book')

    val(top, 'OSSpecific.OperationSpace', fake.sentence(nb_words=4, variable_nb_words=True),
        'Стандартное событие',
        'Operation Space',
        'Стандартное событие',
        'Operation Space')

    val(top, 'OSSpecific.SpecificProcessingRequired', fake.pybool(),
        'Требует специальной обработки БО',
        'Specific BO processing required',
        'На специальную обработку',
        'Specific Processing Required')

    val(top, 'OSSpecific.IsNetting', fake.pybool(),
        'Признак неттинга',
        'Is Netting',
        'Признак неттинга',
        'In Netting')

    val(top, 'OSSpecific.PLItem', fake.sentence(nb_words=2, variable_nb_words=True),
        'Cтатья дохода',
        'PL Item',
        'Cтатья дохода',
        'PL Item')

    val(top, 'OSSpecific.Strategy', fake.sentence(nb_words=3, variable_nb_words=True),
        'Стратегия',
        'Strategy',
        'Стратегия',
        'Strategy')

    val(top, 'OSSpecific.AccountingBasket', fake.sentence(nb_words=3, variable_nb_words=True),
        'Учетная корзина',
        'Acounting Basket',
        'Учетная корзина',
        'Acounting Basket')

    val(top, 'OSSpecific.Version', fake.sentence(nb_words=3, variable_nb_words=True),
        'Версия',
        'Version',
        'Версия',
        'Version')

    val(top, 'BusinessProcess.Roles.Originator', fake.uuid4(),
        'Ориджинатор',
        'Originator',
        'Ориджинатор',
        'Originator')

    val(top, 'BusinessProcess.Roles.SalesManager', fake.uuid4(),
        'Менеджер клиента',
        'Sales manager',
        'Менеджер клиента',
        'Sales manager')

    val(top, 'BusinessProcess.Roles.Trader', fake.uuid4(),
        'Трейдер (Инициатор)',
        'Trader',
        'Трейдер',
        'Trader')

    val(top, 'BusinessProcess.Roles.CtptTrader', fake.uuid4(),
        'Трейдер2',
        'Trader2',
        'Трейдер2',
        'Trader2')

    val(top, 'BusinessProcess.Roles.RiskOfficer', fake.uuid4(),
        'Риск - офицер',
        'Risk - officer',
        'Риск - офицер',
        'Risk - officer')

    val(top, 'BusinessProcess.Roles.Executive', fake.uuid4(),
        'Ответственный исполнитель',
        'Executive',
        'Ответственный исполнитель',
        'Executive')

    val(top, 'BusinessProcess.ConfidentialСomment', fake_local.sentence(nb_words=20, variable_nb_words=True),
        'Конфиденциальный комментарий',
        'Confidential comment',
        'Конф. Комментарий',
        'Conf. Сomment')

    val(top, 'BusinessProcess.STPStatusFO', fake.sentence(nb_words=2),
        'ФО статус',
        'FO status',
        'ФО статус',
        'FO status')

    val(top, 'BusinessProcess.StatusFOA', fake.sentence(nb_words=2),
        'ФО А статус',
        'FO A status',
        'ФО А статус',
        'FO A status')

    val(top, 'BusinessProcess.StatusFOB', fake.sentence(nb_words=2),
        'ФО Б статус',
        'FO B status',
        'ФО Б статус',
        'FO B status')

    val(top, 'BusinessProcess.StatusRisk', fake.sentence(nb_words=2),
        'Риск-статус',
        'Risk-Status',
        'Риск-статус',
        'Risk-Status')

    val(top, 'BusinessProcess.StatusBOPar', fake.sentence(nb_words=2),
        'Статус подготовки БО параметров',
        'BO Parameters Status',
        'Статус подготовки БО параметров',
        'BO Parameters Status')

    val(top, 'BusinessProcess.StatusAccountingAndSettlement', fake.sentence(nb_words=2),
        'Статус учета и расчетов',
        'Accounting and Settlement Status',
        'Статус учета и расчетов',
        'Accounting and Settlement Status')


    return prettify(top)

def generate_eq_fwd():
    top = ET.Element('body')

    val(top, 'ObjModelUID', fake_local.md5(),
        'Универсальный идентификатор объектной модели',
        'Object Model Universal ID',
        'Универсальный ID объектной модел',
        'Object Model Universal ID')

    val(top, 'ObjType', 'Trade',
        'Тип бизнес-объекта',
        'Business-object type',
        'Тип бизнес-объекта',
        'Business-object Type')

    val(top, 'ObjUID', fake_local.uuid4(),
        'Универсальный идентификатор объекта',
        'Business-object Universal ID',
        'Универсальный ID бизнес-объекта',
        'Business-object Universal ID')

    val(top, 'RootObjType', '',
        'Тип бизнес-объекта верхнего уровня',
        'Root business-object type',
        'Тип породившего бизнес-объекта ',
        'Root business-object Type')

    val(top, 'RootObjUID', fake.uuid4(),
        'Универсальный идентификатор объекта верхнего уровня',
        'Root business-object universal ID',
        'Универсальный ID  породившего бизнес-объекта',
        'Root business-object universal ID')

    val(top, 'OriginSystem', fake.bs(),
        'Система происхождения',
        'Origin System',
        'Система происхождения',
        'Origin System')

    val(top, 'OriginSystemID', fake_local.uuid4(),
        'Идентификатор объекта в системе происхождения',
        'Business-object Origin System ID',
        'ID объекта в системе происхождения',
        'Business-object Origin System ID')

    val(top, 'RegDateTime', fake_local.date_time_this_month(before_now=True),
        'Дата и время регистрации',
        'Registration date and time ',
        'Дата и время регистрации',
        'Registration Date and Time')

    val(top, 'BusinessEventType', 'Trade',
        'Тип сделки',
        'Business-event type',
        'Тип бизн.-события',
        'Bus. Event Type')

    val(top, 'EventDateTime', fake_local.date_time_this_month(before_now=True),
        'Дата и время события',
        'Event Date and Time',
        'Дата и время события',
        'Event Date and Time')

    val(top, 'Сomment', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Комментарий',
        'Сomment',
        'Комментарий',
        'Сomment')

    val(top, 'TradeType', 'FWD EQ',
        'Тип сделки',
        'Trade type',
        'Тип сделки',
        'TradeType')

    val(top, 'TradeFloorType', fake_local.pybool(),
        'Тип торговой площадки',
        'Trade Floor Type',
        'Тип торг. площадки',
        'Trade floor type')

    val(top, 'MasterAgreement.RootProductUID', fake_local.uuid4(),
        'Универсальный идентификатор объекта Ген. Соглашения',
        'Master Agreement Universal ID',
        'Универсальный ID объекта Ген. Соглашения',
        'Master Agreement Universal ID')

    val(top, 'MasterAgreement.MasterAgreementNumber', fake_local.pyint(),
        'Номер ген соглашения',
        'Master Agreement Number',
        'Номер ген соглашения',
        'General agreement number')

    val(top, 'MasterAgreement.WithoutMasterAgreement', fake_local.pybool(),
        'Сделка без ГС',
        'Without Master Agreement',
        'Сделка без ГС',
        'Without Master Agreement')

    val(top, 'EventDetails.CorpPaymAsCashFlow', fake_local.pybool(),
        'Поле, которое показывает встраивается ли купон в сделку, либо должен быть выплачен контрагенту',
        'Return corporate payments as cashflow or write off the debt',
        'Корп. выпл.: возврат платежом',
        'Corp. Paym: as CashFlow')

    val(top, 'Participants.Buyer.BuyerNickName', fake_local.profile()['username'],
        'Покупатель',
        'Buyer',
        'Покупатель',
        'Buyer')

    val(top, 'Participants.Seller.SellerNickName', fake_local.profile()['username'],
        'Продавец',
        'Seller',
        'Продавец',
        'Seller')

    val(top, 'Participants.Buyer.LegalEntity.BuyerLegalEntity', fake_local.company(),
        'Юр. Лицо Покупателя',
        'Buyer Legal Entity',
        'Юр. Лицо Покупателя',
        'Buyer LE')

    val(top, 'Participants.Seller.LegalEntity.SellerLegalEntity', fake_local.company(),
        'Юр. Лицо Продавца  ',
        'Seller Legal Entity',
        'Юр. Лицо Продавца  ',
        'Seller LE')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyersBranch', fake.bs(),
        'Подразделение Покупателя',
        'Buyer\'s Branch',
        'Подразделение Покупателя',
        'Buyer\'s Branch')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerProfitCenter', fake.bs(),
        'Профит-центр Покупателя',
        'Buyer\'s Profit center',
        'Профит-центр Покупателя',
        'Buyer\'s Profit center')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerPortfolio', fake.bs(),
        'Портфель Покупателя',
        'Buyer\'s Portfolio',
        'Портфель Покупателя',
        'Buyer\'s Portfolio')

    val(top, 'Participants.Buyer.AccountingRegisters.BuyerBook', fake.uuid4(),
        'Книга Покупателя',
        'Buyer\'s Book',
        'Книга Покупателя',
        'Buyer\'s Book')

    val(top, 'Participants.Seller.AccountingRegisters.SellersBranch', fake.uuid4(),
        'Подразделение Продавца',
        'Seller\'s Branch',
        'Подразделение Продавца',
        'Seller\'s Branch')

    val(top, 'Participants.Seller.AccountingRegisters.SellerProfitCenter', fake.uuid4(),
        'Профит-центр Продавца',
        'Seller\'s Profit center',
        'Профит-центр Продавца',
        'Seller\'s Profit center')

    val(top, 'Participants.Seller.AccountingRegisters.SellerPortfolio', fake.uuid4(),
        'Портфель Продавца',
        'Seller\'s Portfolio',
        'Портфель Продавца',
        'Seller\'s Portfolio')

    val(top, 'Participants.Seller.AccountingRegisters.SellerBook', fake.uuid4(),
        'Книга Продавца',
        'Seller\'s Book',
        'Книга Продавца',
        'Seller\'s Book')

    val(top, 'Participants.Buyer.BuyersTraderName', fake_local.name(),
        'Имя Трейдера со стороны Покупателя',
        'Buyer\'s Trader Name',
        'Имя Трейдера (Пок.)',
        'Buyer\'s Trader Name')

    val(top, 'Participants.Seller.SellersTraderName', fake_local.name(),
        'Имя Трейдера со стороны Продавца',
        'Seller\'s Trader Name',
        'Имя Трейдера (Прод.)',
        'Seller\'s Trader Name')

    val(top, 'EventDetails.TradeDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата сделки',
        'Trade Date',
        'Дата сделки',
        'Trade Date')

    val(top, 'EventDetails.MaturityType', 'None',
        'Срочность сделки',
        'Maturity Type',
        'Срочность сделки',
        'Maturity Type')

    val(top, 'EventDetails.MaturityDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата завершения обязательств по сделке',
        'Maturity Date',
        'Дата завершения',
        'Maturity Date')

    val(top, 'EventDetails.SettlementMode', 'On foot',
        'Способ поставки',
        'Settlement Mode',
        'Способ поставки',
        'Settlement Mode')

    val(top, 'EventDetails.UnderlyingType', fake.sentence(nb_words=2),
        'Тип базового актива',
        'Underlying Type',
        'Тип инструмента',
        'Underlying Type')

    val(top, 'EventDetails.UnderlyingUID', fake.uuid4(),
        'Универсальный идентификатор базового актива',
        'Underlying asset universal ID',
        '-',
        '-')

    val(top, 'EventDetails.Underlying', fake.sentence(nb_words=2),
        'Базовый актив',
        'Underlying asset',
        'Инструмент',
        'Underlying')

    val(top, 'EventDetails.ISIN', fake.uuid4(),
        'ISIN',
        'ISIN',
        'ISIN',
        'ISIN')

    val(top, 'EventDetails.DomesticCode', fake.pyint(),
        'Национальный код инструмента',
        'Underlying Domestic Code',
        'Национальный код инструмента',
        'Underlying Domestic Code')

    val(top, 'EventDetails.UnderlyingCcy', fake.currency_code(),
        'Валюта номинала',
        'Underlying сurrency',
        'Валюта инструмента',
        'Instrument Ccy')

    val(top, 'EventDetails.UnderlyingQty', fake.pyint() % 5000,
        'Количество базового актива',
        'Quantity of Underlying Asset',
        'Количество ',
        'Quantity')

    val(top, 'EventDetails.QuantityUnits', 'Units',
        'Единицы номингирования (в чем выражается количество)',
        'Quantity units',
        '-',
        '-')

    val(top, 'EventDetails.TradePrice', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Цена заключения сделки за единицу базового актива в валюте переоценки ',
        'Trade price per the unit of Underlying Asset',
        'Цена заключения сделки',
        'Trade Price in Trade Pricing Ccy per the unit of Underlying Asset')

    val(top, 'EventDetails.QuoteUnits', 'None',
        'Единицы переоценки ',
        'Quote Units',
        'Единицы переоценки',
        'Quote Units')

    val(top, 'EventDetails.UnderlyingValueUnderlyingCcy', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Эквивалентная стоимость базового актива в валюте номинала',
        'Underluying asset value in underlying currency',
        'Стоим. Баз. актива в валюте номинала',
        'Value in Pricing Ccy')

    val(top, 'EventDetails.PaymentCcy', fake.currency_code(),
        'Валюта расчетов по сделке',
        'Payment Ccy',
        'Вал. расч. ',
        'Paym. Ccy')

    val(top, 'EventDetails.CnvRateUnderlCcyPaymCcy', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Курс конвертации из валюты базового актива в валюту расчетов.',
        'Rate to convert from Underluying Ccy to  Payment Ccy',
        'Курс. Конв. ([CcyPair])',
        'Cnv. Rate ([CcyPair])')

    val(top, 'EventDetails.CnvCcyPairUnderlCcyPaymCcy', fake_local.pyfloat(left_digits=2, right_digits=2, positive=True),
        'Валютная пара валюты базового актива и валюты расчетов',
        'Ccy Pair for Underluying Ccy and Payment Ccy',
        '-',
        '-')

    val(top, 'EventDetails.AmountDuePaymCcy', fake_local.pyfloat(left_digits=5, right_digits=2, positive=True),
        'Сумма к выплате в валюте расчетов',
        'Amount Due in payment currency',
        'Сумма к выпл. в вал. расч.',
        'Amount Due in Paym. Ccy')

    val(top, 'SettlementConditions.DeliveryTerms', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Последовательность поставки',
        'Delivery Terms',
        'Последовательность поставки',
        'Delivery Terms')

    val(top, 'SettlementConditions.DeliveryDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата поставки',
        'Delivery Date',
        'Дата поставки',
        'Delivery Date')

    val(top, 'SettlementConditions.ValueDate', fake_local.date_time_this_month(before_now=True).date(),
        'Дата оплаты ',
        'Value Date',
        'Дата оплаты',
        'Value Date')

    val(top, 'SettlementConditions.RuleToDefineStandardValueDate', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Правило определения стандартной даты расчетов',
        'Rule to define standard value date',
        'Правило определения стандартной даты расчетов',
        'Rule to Define Std. Val. Date')

    val(top, 'SettlementConditions.HolidaysCalendar', fake_local.sentence(nb_words=12, variable_nb_words=True),
        'Календарь праздников и выходных дат. Задается в форме перечня активов',
        'расписание праздников по которым требуется включить в календарь сделки.',
        'Holidays calendar. Calendar is set as a list of assets whose holidays schedules should be included to the calendar of the deal',
        'Календарь праздн. И вых. Дней,Holidays Calendar')

    val(top, 'SettlementConditions.CustodianToDeliverFrom', fake_local.company(),
        'Депозитарий, через который производится поставка',
        'Custodian to Deliver from',
        'Депозитарий для поставки',
        'Custodian to Deliver from')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientsBranch', fake.bs(),
        'Подразделение Получателя платежа',
        'Cashflow recepient\'s Branch',
        'Подразделение Получателя платежа',
        'Recepient\'s Branch')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientProfitCenter', fake.bs(),
        'Профит-центр Получателя платежа',
        'Cashflow recepient\'s Profit center',
        'Профит-центр Получателя платежа',
        'Recepient\'s Profit center')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientPortfolio', fake.uuid4(),
        'Портфель Получателя платежа',
        'Cashflow recepient\'s Portfolio',
        'Портфель Получателя платежа',
        'Recepient\'s Portfolio')

    val(top, 'Participants.CSRecepient.AccountingRegisters.CSRecepientBook', fake.uuid4(),
        'Книга Получателя платежа',
        'Cashflow recepient\'s Book',
        'Книга Получателя платежа',
        'Recepient\'s Book')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayersBranch', fake.uuid4(),
        'Подразделение Отправителя платежа',
        'Cashflow payer\'s Branch',
        'Подразделение Отправителя платежа',
        'Payer\'s Branch')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayerProfitCenter', fake.bs(),
        'Профит-центр Отправителя платежа',
        'Cashflow payer\'s Profit center',
        'Профит-центр Отправителя платежа',
        'Payer\'s Profit center')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayerPortfolio', fake.uuid4(),
        'Портфель Отправителя платежа',
        'Cashflow payer\'s Portfolio',
        'Портфель Отправителя платежа',
        'Payer\'s Portfolio')

    val(top, 'Participants.CSPayer.AccountingRegisters.CSPayerBook', fake.uuid4(),
        'Книга Отправителя платежа',
        'Cashflow payer\'s Book',
        'Книга Отправителя платежа',
        'Payer\'s Book')

    val(top, 'OSSpecific.OperationSpace', fake.sentence(nb_words=4, variable_nb_words=True),
        'Стандартное событие',
        'Operation Space',
        'Стандартное событие',
        'Operation Space')

    val(top, 'OSSpecific.SpecificProcessingRequired', fake.pybool(),
        'Требует специальной обработки БО',
        'Specific BO processing required',
        'На специальную обработку',
        'Specific Processing Requiredn')

    val(top, 'OSSpecific.IsNetting', fake.pybool(),
        'Признак неттинга',
        'Is Netting',
        'Признак неттинга',
        'In Netting')

    val(top, 'OSSpecific.PLItem', fake.sentence(nb_words=2, variable_nb_words=True),
        'Cтатья дохода',
        'PL Item',
        'Cтатья дохода',
        'PL Item')

    val(top, 'OSSpecific.Strategy', fake.sentence(nb_words=3, variable_nb_words=True),
        'Стратегия',
        'Strategy',
        'Стратегия',
        'Strategy')

    val(top, 'OSSpecific.AccountingBasket', fake.sentence(nb_words=3, variable_nb_words=True),
        'Учетная корзина',
        'Acounting Basket',
        'Учетная корзина',
        'Acounting Basket')

    val(top, 'OSSpecific.Version', fake.sentence(nb_words=3, variable_nb_words=True),
        'Версия',
        'Version',
        'Версия',
        'Version')

    val(top, 'BusinessProcess.Roles.Originator', fake.uuid4(),
        'Ориджинатор',
        'Originator',
        'Ориджинатор',
        'Originator')

    val(top, 'BusinessProcess.Roles.SalesManager', fake.uuid4(),
        'Менеджер клиента',
        'Sales manager',
        'Менеджер клиента',
        'Sales manager')

    val(top, 'BusinessProcess.Roles.Trader', fake.uuid4(),
        'Трейдер (Инициатор)',
        'Trader',
        'Трейдер',
        'Trader')

    val(top, 'BusinessProcess.Roles.CtptTrader', fake.uuid4(),
        'Трейдер2',
        'Trader2',
        'Трейдер2',
        'Trader2')

    val(top, 'BusinessProcess.Roles.RiskOfficer', fake.uuid4(),
        'Риск - офицер',
        'Risk - officer',
        'Риск - офицер',
        'Risk - officer')

    val(top, 'BusinessProcess.Roles.Executive', fake.uuid4(),
        'Ответственный исполнитель',
        'Executive',
        'Ответственный исполнитель',
        'Executive')

    val(top, 'BusinessProcess.ConfidentialСomment', fake_local.sentence(nb_words=20, variable_nb_words=True),
        'Конфиденциальный комментарий',
        'Confidential comment',
        'Конф. Комментарий',
        'Conf. Сomment')

    val(top, 'BusinessProcess.STPStatusFO', fake.sentence(nb_words=2),
        'ФО статус',
        'FO status',
        'ФО статус',
        'FO status')

    val(top, 'BusinessProcess.StatusFOA', fake.sentence(nb_words=2),
        'ФО А статус',
        'FO A status',
        'ФО А статус',
        'FO A status')

    val(top, 'BusinessProcess.StatusFOB', fake.sentence(nb_words=2),
        'ФО Б статус',
        'FO B status',
        'ФО Б статус',
        'FO B status')

    val(top, 'BusinessProcess.StatusRisk', fake.sentence(nb_words=2),
        'Риск-статус',
        'Risk-Status',
        'Риск-статус',
        'Risk-Status')

    val(top, 'BusinessProcess.StatusBOPar', fake.sentence(nb_words=2),
        'Статус подготовки БО параметров',
        'BO Parameters Status',
        'Статус подготовки БО параметров',
        'BO Parameters Status')

    val(top, 'BusinessProcess.StatusAccountingAndSettlement', fake.sentence(nb_words=2),
        'Статус учета и расчетов',
        'Accounting and Settlement Status',
        'Статус учета и расчетов',
        'Accounting and Settlement Status')

    return prettify(top)

def usage():
    print("gen.py fx|fx_fwd|eq_fwd")
    os.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    if sys.argv[1] == 'fx':
        print(generate_fx())
    elif sys.argv[1] == 'fx_fwd':
        print(generate_fx_fwd())
    elif sys.argv[1] == 'eq_fwd':
        print(generate_eq_fwd())
    else:
        usage()

if __name__ == '__main__':
    main()
