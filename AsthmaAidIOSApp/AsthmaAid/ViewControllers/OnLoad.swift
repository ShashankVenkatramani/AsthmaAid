//
//  OnLoad.swift
//  AsthmaAid
//
//  Created by Shanky(Prgm) on 3/12/19.
//  Copyright © 2019 Shashank Venkatramani. All rights reserved.
//

import UIKit

class OnLoad: UIViewController {
    @IBOutlet weak var Doctors: SecondaryButton!
    @IBOutlet weak var Patients: SecondaryButton!
    
    @IBAction func doctorsPressed(_ sender: Any) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "LoginDoctor") as! LoginDoctor
        present(vc, animated: false, completion: nil)
    }
    @IBAction func patientsPressed(_ sender: Any) {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "LoginStudent") as! LoginStudent
        present(vc, animated: false, completion: nil)
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

}
