//
//  LoginStudent.swift
//  AsthmaAid
//
//  Created by Shanky(Prgm) on 3/12/19.
//  Copyright © 2019 Shashank Venkatramani. All rights reserved.
//

import UIKit
import FirebaseAuth

class LoginStudent: UIViewController {
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    
    @IBAction func loginPressed(_ sender: Any) {
        Auth.auth().signIn(withEmail: emailField!.text!, password: passwordField!.text!) { (user, error) in
            if let user = user {
                let storyboard = UIStoryboard(name: "Main", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "DataCaptureTest") as! DataCaptureTest
                vc.uid = user.user.uid
                self.present(vc, animated: false, completion: nil)
            }
        }
        
    }
    @IBAction func registerPressed(_ sender: Any) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "StudentRegister") as! StudentRegister
        self.present(vc, animated: false, completion: nil)
    }
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
    }
}
