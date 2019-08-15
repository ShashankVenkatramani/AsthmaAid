//
//  DataCaptureTest.swift
//  AsthmaAid
//
//  Created by Shanky(Prgm) on 3/11/19.
//  Copyright © 2019 Shashank Venkatramani. All rights reserved.
//
// Tried remove all for breath data
import UIKit
import CoreBluetooth
import Firebase
import FirebaseDatabase
import Charts
class DataCaptureTest: UIViewController, CBCentralManagerDelegate, CBPeripheralDelegate, ChartViewDelegate/*, UITableViewDataSource, UITableViewDelegate */{
    @IBOutlet weak var LineChart: LineChartView!
    @IBOutlet weak var dayChart: UIView!
    @IBOutlet weak var monthChart: UIView!
    @IBOutlet weak var yearChart: UIView!
    
    
    var lowerLimit: Double = 500
    var upperLimit: Double = 900
    var range: Double = 400
    var centralManager: CBCentralManager!
    var peripherals: [CBPeripheral] = []
    var rssis: [NSNumber] = []
    var sensorBLE: CBPeripheral?
    var dataIsBeingRead:Bool = false
    var clock = Timer()
    var currentCount:Int = 0
    var breathData: [NSString] = []
    var reference:DatabaseReference = Database.database().reference()
    var uid:String?
    var counter:Int = 0
    var dataCount:Int = 0
    
    var lineDataEntry: [ChartDataEntry] = []
    
    var milliseconds = [Double]()
    var value = [Double]()
    
    var dayGoodEntry = PieChartDataEntry(value: 0)
    var dayBadEntry = PieChartDataEntry(value: 0)
    
    override func viewDidLoad() {
        milliseconds.removeAll()
        self.value.removeAll()
        
        super.viewDidLoad()
        clock = Timer.scheduledTimer(timeInterval: 1, target: self, selector: (#selector(self.updateTimer)), userInfo: nil, repeats: true)
        centralManager = CBCentralManager(delegate: self, queue: nil)
        LineChart.animate(xAxisDuration: 2.0, yAxisDuration: 2.0)
        
    }
    
    @objc func updateTimer(){
        if(dataIsBeingRead){
            currentCount += 1
        }
        if(currentCount > 10){
            currentCount = 0
            let data = [uid, breathData] as [Any]
            self.reference.child("requests").child(randomHash(length: 8)).setValue(data)
            breathData.removeAll()
        }
    }
    
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if(central.state != CBManagerState.poweredOn){
            let bluetoothRequestVC = UIAlertController(title: "Bluetooth is disabled}", message: "For full app functionality, please turn on bluetooth", preferredStyle: UIAlertController.Style.alert)
            let ok = UIAlertAction(title: "ok", style: UIAlertAction.Style.default) { (action) in
                self.dismiss(animated: true, completion: nil)
            }
            bluetoothRequestVC.addAction(ok)
            self.present(bluetoothRequestVC, animated: true, completion: nil)
        } else {
            startScan()
        }
    }
    
    func startScan() {
        centralManager.scanForPeripherals(withServices: [CBUUID(string: "FFE0")], options: [CBCentralManagerScanOptionAllowDuplicatesKey : false])
    }
    
    
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        self.peripherals.append(peripheral)
        peripheral.delegate = self
        peripheral.discoverServices([CBUUID(string: "FFE0")])
        self.rssis.append(RSSI)
        self.sensorBLE = peripheral
        centralManager?.connect(self.sensorBLE!, options: nil)
    }
    
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral){
        centralManager.stopScan()
        
        peripheral.delegate = self
        peripheral.discoverServices([CBUUID(string: "FFE0")])
        
    }
    
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        guard let services = peripheral.services else {
            print("services failed")
            return
        }
        
        for service in services {
            peripheral.discoverCharacteristics(nil, for: service)
        }
        print("services found")
        print(services)
    }
    
    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        print("called characteristics")
        if(error != nil){
            print("charactersitics failed")
        }
        
        guard let characteristics = service.characteristics else {
            return
        }
        print("Characterstics: ")
        for characteristic in characteristics{
            print(characteristic.uuid)
            peripheral.discoverDescriptors(for: characteristic)
            peripheral.setNotifyValue(true, for: characteristic)
        }
    }
    
    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        counter = counter + 1
        if(!dataIsBeingRead){
            dataIsBeingRead = true
        } else {
            
        }
        if let string = NSString(data: characteristic.value!, encoding: String.Encoding.utf8.rawValue) {
            //print(string)
            breathData.append(string)
            
            var value:String = ""
            var readBool:Bool = false
            var ms:String = ""
            let stringValue = string as String
            for index in stringValue.indices {
                if(readBool){
                    value = value + String(stringValue[index])
                } else {
                    if(stringValue[index] == ","){
                        readBool = true
                    } else {
                        ms = ms + String(stringValue[index])
                    }
                }
            }
            if(counter % 10 == 0){
                self.milliseconds.append((ms as NSString).doubleValue)
                self.value.append((value as NSString).doubleValue)
            }
            if(counter % 100 == 0){
                setUpChart()
                milliseconds.removeAll()
                self.value.removeAll()
            }
            //print(ms)
        }
    }
    
    func setUpChart() {
        lineDataEntry.removeAll()
        for i in milliseconds.count - 10..<milliseconds.count {
            let dataPoint = ChartDataEntry(x: milliseconds[i], y: value[i])
            lineDataEntry.append(dataPoint)
        }
        
        let chartDataSet = LineChartDataSet(values: lineDataEntry, label: "Breath")
        let chartData = LineChartData()
        chartData.addDataSet(chartDataSet)
        chartData.setDrawValues(false)
        chartDataSet.colors = [colors.primaryGreen]
        chartDataSet.setCircleColor(colors.primaryGreen)
        chartDataSet.circleHoleColor = colors.primaryGreen
        chartDataSet.circleRadius = 2
        
        
        
        chartDataSet.fill = Fill.fillWithColor(colors.primaryGreen)
        chartDataSet.drawFilledEnabled = true
        
        
        LineChart.data = chartData
    }
    
    func setColors() {
        view.backgroundColor = colors.backgroundColor
    }
    
    func changeBackground(string:String) {
        //8 38 58
        //10 58 120
        var value:String = ""
        var readBool:Bool = false
        for index in string.indices {
            if(readBool){
                value = value + String(string[index])
            }
            if(string[index] == ","){
                readBool = true
            }
        }
        //print("value: " + value)
        var stretchDistance = (value as NSString).doubleValue
        if(stretchDistance != nil){
            var colorFactor = (stretchDistance - lowerLimit)/(upperLimit - lowerLimit)
            if(colorFactor < 1 && colorFactor > 0){
                view.backgroundColor = UIColor(red: CGFloat(8 + 2*colorFactor)/255, green: CGFloat(38 + colorFactor*20)/255, blue: CGFloat(58 + colorFactor*62)/255, alpha: 1)
            }
        }
        
    }
    
    func randomHash(length: Int) -> String {
        let letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return String((0..<length).map{ _ in letters.randomElement()! })
    }
}
