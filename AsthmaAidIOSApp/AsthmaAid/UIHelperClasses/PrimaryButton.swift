//
//  PrimaryButton.swift
//  AsthmaAid
//
//  Created by Shanky(Prgm) on 3/12/19.
//  Copyright © 2019 Shashank Venkatramani. All rights reserved.
//

import UIKit

class PrimaryButton: UIButton {
    required init?(coder a: NSCoder){
        super.init(coder: a)
        setup()
    }
    
    private func setup() {
        backgroundColor = colors.primaryGreen
        setTitleColor(UIColor.white, for: .normal)
        layer.cornerRadius = 25
        titleLabel?.font = UIFont(name: "AvenirNext-Bold", size: 25.0)
        
        layer.shadowColor = colors.primaryGreen.cgColor
        layer.shadowOffset = CGSize(width: 7, height: 5)
        layer.shadowRadius = 10
        layer.shadowOpacity = 0.3
        
    }
}
