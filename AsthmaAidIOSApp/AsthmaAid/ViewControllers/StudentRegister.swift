//
//  StudentRegister.swift
//  AsthmaAid
//
//  Created by Shanky(Prgm) on 3/12/19.
//  Copyright © 2019 Shashank Venkatramani. All rights reserved.
//

import UIKit
import Firebase
import FirebaseAuth
import FirebaseDatabase
class StudentRegister: UIViewController {
    var ref:DatabaseReference = Database.database().reference()
    
    @IBOutlet weak var fullName: UITextField!
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    @IBOutlet weak var doctorIdField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func registerPressed(_ sender: Any) {
        let fullNameText = fullName!.text
        let email = emailField!.text
        let password = passwordField!.text
        let doctorID = doctorIdField!.text
        
        ref.child("doctors").observeSingleEvent(of: .value) { (snapshot) in
            let doctorArray = snapshot.value as! NSMutableArray
        }
        
        Auth.auth().createUser(withEmail: email!, password: password!) { (user, error) in
            if let user = user {
                let data = [fullNameText, email, doctorID]
                self.ref.child("patients").child(user.user.uid).child("info").setValue(data)
                let storyboard = UIStoryboard(name: "Main", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "DataCaptureTest") as! DataCaptureTest
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
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
    }
}
