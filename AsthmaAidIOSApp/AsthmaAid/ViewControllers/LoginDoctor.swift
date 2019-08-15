//
//  LoginDoctor.swift
//  AsthmaAid
//
//  Created by Shanky(Prgm) on 3/14/19.
//  Copyright © 2019 Shashank Venkatramani. All rights reserved.
//

import UIKit
import Firebase
import FirebaseAuth

class LoginDoctor: UIViewController {
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    @IBAction func loginPressed(_ sender: Any) {
        Auth.auth().signIn(withEmail: emailField!.text!, password: passwordField!.text!) { (user, error) in
            if let user = user {
                let storyboard = UIStoryboard(name: "Main", bundle: nil)
                let vc = storyboard.instantiateViewController(withIdentifier: "DoctorDashboard") as! DoctorDashboard
                vc.uid = user.user.uid
                self.present(vc, animated: false, completion: nil)
            }
        }
    }
    @IBAction func registerPressed(_ sender: Any) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "DoctorRegister") as! DoctorRegister
        self.present(vc, animated: false, completion: nil)
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
    }
}
