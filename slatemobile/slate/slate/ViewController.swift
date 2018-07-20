//
//  ViewController.swift
//  slate
//
//  Created by Gregory Gundersen on 7/19/18.
//  Copyright © 2018 Gregory Gundersen. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var costTextField: UITextField!
    @IBOutlet weak var categoryTextField: UITextField!
    @IBOutlet weak var commentTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func submitExpenseBtn(_ sender: Any) {
        NSLog("Submit button pressed");
        let commentStr = self.commentTextField.text!
        NSLog(commentStr);
    }
}

