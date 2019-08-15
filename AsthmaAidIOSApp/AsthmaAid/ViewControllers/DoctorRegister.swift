//
//  DoctorRegister.swift
//  AsthmaAid
//
//  Created by Shanky(Prgm) on 3/14/19.
//  Copyright © 2019 Shashank Venkatramani. All rights reserved.
//

import UIKit
import FirebaseAuth
import FirebaseDatabase
import Firebase
class DoctorRegister: UIViewController {
    @IBOutlet weak var fullNameField: UITextField!
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    
    var ref:DatabaseReference = Database.database().reference()
    
    @IBAction func registerPressed(_ sender: Any) {
        let fullNameText = fullNameField!.text
        let email = emailField!.text
        let password = passwordField!.text
        Auth.auth().createUser(withEmail: email!, password: password!) { (user, error) in
            if let user = user {
                let hash = self.randomHash(length: 5)
                let data = [fullNameText, email, hash, ["default"]] as [Any]
                self.ref.child("doctors").child(user.user.uid).child("info").setValue(data)
                let storyboard = UIStoryboard(name: "Main", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "DoctorDashboard") as! DoctorDashboard
                vc.uid = user.user.uid
                self.present(vc, animated: false, completion: nil)
            } else {
                /*
                 let alertVC = UIAlertController(title: "Register Failed", message: , preferredStyle: UIAlertController.Style.alert)
                 let ok = UIAlertAction(title: "ok", style: UIAlertAction.Style.default, handler: { (action) in
                 self.dismiss(animated: true, completion: nil)
                 })
                 alertVC.addAction(ok)
                 self.present(alertVC, animated: false, completion: nil)
                 */
            }
        }
    }
    
    func randomHash(length: Int) -> String {
        let letters = "abcdefghijklmnpqrstuvwxyz123456789"
        return String((0..<length).map{ _ in letters.randomElement()! })
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
    }
}
