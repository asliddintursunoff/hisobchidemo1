def int_to_month_string_uz(month):
    months = [
        "Январ", "Феврал", "Март", "Апрел", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    return months[month - 1] if 1 <= month <= 12 else "мавжуд бўлмаган сана"


def calculating_total_sum(worker,progress_filtered,ProgressItem):
    sum_info=[]
    for i in worker:     
        worker_total_sum = 0
        for j in progress_filtered.filter(worker = i):
           
            price = j.work.price
            a = 0
            for table in ProgressItem.objects.filter(progress=j):               
                a+=table.number 
            sum = a*price
            worker_total_sum+=sum    
        print("",worker_total_sum)
        content = {
            "people":i,
            "people_id":i.id,
            "sum_money": worker_total_sum,
        }
        sum_info.append(content)
    return sum_info



def total_work_number(works,progress):
        total_work = []
        for w in works:
            actual_progress_items = progress.filter(work = w)
            total= 0
            for a in actual_progress_items:
                
                total+=a.total_work_done
            total_dict = {
                "work_id":w.id,
                "work_n":w,
                "total":total
            }
            total_work.append(total_dict)
        return total_work
    
def total_sum_money(calculating_total_sum):
    sum = 0
    for i in calculating_total_sum:
        sum+=i["sum_money"]
        
    return sum
    